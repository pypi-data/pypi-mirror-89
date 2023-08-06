import scipy
import numpy
import heapq
import statsmodels.stats.multitest

import time
import sys
import collections
import functools

hasR = False
try:
    import rpy2.robjects
    hasR = True
except Exception as e:
    hasR = False

if hasR:
    from rpy2.robjects import r, DataFrame, globalenv, IntVector, FloatVector, StrVector, packages as rpackages

from pytransit.analysis import base
import pytransit
import pytransit.transit_tools as transit_tools
import pytransit.tnseq_tools as tnseq_tools
import pytransit.norm_tools as norm_tools

############# GUI ELEMENTS ##################

short_name = "ZINB"
long_name = "ZINB"
short_desc = "Perform ZINB analysis"
long_desc = """Perform ZINB analysis"""
EOL = "\n"
DEBUG = False
GENE = None
SEPARATOR = '\1' # for making names that combine conditions and interactions; try not to use a char a user might have in a condition name

transposons = ["", ""]
columns = []

class ZinbAnalysis(base.TransitAnalysis):
    def __init__(self):
        base.TransitAnalysis.__init__(self, short_name, long_name, short_desc, long_desc, transposons, ZinbMethod)
def main():
  print("ZINB example")

class ZinbMethod(base.MultiConditionMethod):
    """
    Zinb
    """
    def __init__(self, combined_wig, metadata, annotation, normalization, output_file, ignored_conditions=[], included_conditions=[], winz=False, nterm=5.0, cterm=5.0, condition="Condition", covars=[], interactions = []):
        base.MultiConditionMethod.__init__(self, short_name, long_name, short_desc, long_desc, combined_wig, metadata, annotation, output_file,
                normalization=normalization, ignored_conditions=ignored_conditions, included_conditions=included_conditions, nterm=nterm, cterm=cterm)
        self.winz = winz
        self.covars = covars
        self.interactions = interactions
        self.condition = condition

    @classmethod
    def transit_error(self,msg): print("error: %s" % msg) # for some reason, transit_error() in base class or transit_tools doesn't work right; needs @classmethod

    @classmethod
    def fromargs(self, rawargs):
        if not hasR:
            print("Error: R and rpy2 (~= 3.0) required to run ZINB analysis.")
            print("After installing R, you can install rpy2 using the command \"pip install 'rpy2~=3.0'\"")
            sys.exit(0)

        (args, kwargs) = transit_tools.cleanargs(rawargs)

        if (kwargs.get('-help', False) or kwargs.get('h', False)):
            print(ZinbMethod.usage_string())
            sys.exit(0)

        if (kwargs.get('v', False)):
            global DEBUG
            DEBUG = True

        if (kwargs.get('-gene', False)):
            global GENE
            GENE = kwargs.get('-gene', None)

        combined_wig = args[0]
        metadata = args[1]
        annotation = args[2]
        output_file = args[3]
        normalization = kwargs.get("n", "TTR")
        NTerminus = float(kwargs.get("iN", 5.0))
        CTerminus = float(kwargs.get("iC", 5.0))
        condition = kwargs.get("-condition", "Condition")
        covars = list(filter(None, kwargs.get("-covars", "").split(",")))
        interactions = list(filter(None, kwargs.get("-interactions", "").split(",")))
        winz = True if "w" in kwargs else False
        ignored_conditions = list(filter(None, kwargs.get("-ignore-conditions", "").split(",")))
        included_conditions = list(filter(None, kwargs.get("-include-conditions", "").split(",")))

        # check for unrecognized flags
        flags = "-n --ignore-conditions --include-conditions -iN -iC --condition --covars --interactions --gene".split()
        for arg in rawargs:
          if arg[0]=='-' and arg not in flags:
            self.transit_error("flag unrecognized: %s" % arg)
            print(ZinbMethod.usage_string())
            sys.exit(0)

        return self(combined_wig, metadata, annotation, normalization, output_file, ignored_conditions, included_conditions, winz, NTerminus, CTerminus, condition, covars, interactions)

    def wigs_to_conditions(self, conditionsByFile, filenamesInCombWig):
        """
            Returns list of conditions corresponding to given wigfiles.
            ({FileName: Condition}, [FileName]) -> [Condition]
            Condition :: [String]
        """
        return [conditionsByFile.get(f, self.unknown_cond_flag) for f in filenamesInCombWig]

    # the following 2 functions seem redundant and could be merged...

    def wigs_to_covariates(self, covariatesMap, filenamesInCombWig):
        """
            Returns list of covariate lists. Each covariate list consists of covariates corresponding to given wigfiles.
            ([{FileName: Covar}], [FileName]) -> [[Covar]]
            Covar :: String
        """
        try:
            return [[covarsByFile.get(f,"?")
                        for f in filenamesInCombWig]
                        for covarsByFile in covariatesMap]
        except KeyError:
            #self.transit_error("Error: Covariates not found for file {0}".format(f))
            self.transit_error("Error: Covariates not found for sample:")
            for f in filenamesInCombWig:
              if f not in covariatesMap[0]: print(f)
            sys.exit(0)

    def wigs_to_interactions(self, interactionsMap, filenamesInCombWig):
        """
            Returns list of interaction lists. Each interaction list consists of covariates corresponding to given wigfiles.
            ([{FileName: Interaction}], [FileName]) -> [[Interaction]]
            Interaction :: String
        """
        try:
            return [[covarsByFile.get(f,"?")
                        for f in filenamesInCombWig]
                        for covarsByFile in interactionsMap]
        except KeyError:
            #self.transit_error("Error: Interaction var not found for file {0}".format(f))
            self.transit_error("Error: Interaction var not found for sample")
            for f in filenamesInCombWig:
              if f not in interactionsMap[0]: print(f)
            sys.exit(0)

    def stats_for_gene(self, siteIndexes, groupWigIndexMap, data):
        """
            Returns a dictionary of {Group: {Mean, NzMean, NzPerc}}
            ([SiteIndex], [Condition], [WigData]) -> [{Condition: Number}]
            SiteIndex :: Number
            WigData :: [Number]
            Group :: String (combination of '<interaction>_<condition>')
        """
        nonzero = lambda xs: xs[numpy.nonzero(xs)]
        nzperc = lambda xs: numpy.count_nonzero(xs)/float(xs.size)

        means = {}
        nz_means = {}
        nz_percs = {}

        for (group, wigIndexes) in groupWigIndexMap.items():
            if (len(siteIndexes) == 0): # If no TA sites, write 0
                means[group] = 0
                nz_means[group] = 0
                nz_percs[group] = 0
            else:
                arr = data[wigIndexes][:, siteIndexes]
                means[group] = numpy.mean(arr) if len(arr) > 0 else 0
                nonzero_arr = nonzero(arr)
                nz_means[group] = numpy.mean(nonzero_arr) if len(nonzero_arr) > 0 else 0
                nz_percs[group] = nzperc(arr)

        return {'mean': means, 'nz_mean': nz_means, 'nz_perc': nz_percs}

    def stats_by_rv(self, data, RvSiteindexesMap, genes, conditions, interactions):
        """
            Returns Dictionary of Stats by condition for each Rv
            ([[Wigdata]], {Rv: SiteIndex}, [Gene], [Condition], [Interaction]) -> {Rv: {Condition: Number}}
            Wigdata :: [Number]
            SiteIndex :: Number
            Gene :: {start, end, rv, gene, strand}
            Condition :: String
            Interaction :: String
        """

        ## Group wigfiles by (interaction, condition) pair
        ## {'<interaction>_<condition>': [Wigindexes]}
        groupWigIndexMap = collections.defaultdict(lambda: [])
        for i, conditionForWig in enumerate(conditions):
            if (len(interactions) > 0):
                for interaction in interactions:
                    groupName = conditionForWig + SEPARATOR + interaction[i] 
                    groupWigIndexMap[groupName].append(i)
            else:
                groupName = conditionForWig
                groupWigIndexMap[groupName].append(i)

        statsByRv = {}
        for gene in genes:
            Rv = gene["rv"]
            statsByRv[Rv] = self.stats_for_gene(RvSiteindexesMap[Rv], groupWigIndexMap, data)

        ## TODO :: Any ordering to follow?
        statGroupNames = groupWigIndexMap.keys()
        return statsByRv, statGroupNames

    def global_stats_for_rep(self, data):
        """
        Returns the logit zero percentage and nz_mean for each replicate.
            [[WigData]] -> [[Number] ,[Number]]
        """

        logit_zero_perc = []
        nz_mean = []
        for wig in data:
            zero_perc = (wig.size - numpy.count_nonzero(wig))/float(wig.size)
            logit_zero_perc.append(numpy.log(zero_perc/(1 - zero_perc)))
            nz_mean.append(numpy.mean(wig[numpy.nonzero(wig)]))
        return [numpy.array(logit_zero_perc), numpy.array(nz_mean)]

    def group_by_condition(self, wigList, conditions):
        """
            Returns array of datasets, where each dataset corresponds to one condition.
            ([[Wigdata]], [Condition]) -> [[DataForCondition]]
            Wigdata :: [Number]
            Condition :: String
            DataForCondition :: [Number]
        """
        countsByCondition = collections.defaultdict(lambda: [])
        for i, c in enumerate(conditions):
          countsByCondition[c].append(wigList[i])

        return [numpy.array(v).flatten() for v in countsByCondition.values()]

    def melt_data(self, readCountsForRv, conditions, covariates, interactions, NZMeanByRep, LogZPercByRep):
        rvSitesLength = len(readCountsForRv[0])
        repeatAndFlatten = lambda xs: numpy.repeat(xs, rvSitesLength)

        return [
                numpy.concatenate(readCountsForRv).astype(int),
                repeatAndFlatten(conditions),
                list(map(repeatAndFlatten, covariates)),
                list(map(repeatAndFlatten, interactions)),
                repeatAndFlatten(NZMeanByRep),
                repeatAndFlatten(LogZPercByRep)
               ]

    def def_r_zinb_signif(self):
        r('''
            zinb_signif = function(df,
                zinbMod1,
                zinbMod0,
                nbMod1,
                nbMod0, DEBUG = F) {
              suppressMessages(require(pscl))
              suppressMessages(require(MASS))
              melted = df

              # filter out genes that have low saturation across all conditions, since pscl sometimes does not fit params well (resulting in large negative intercepts and high std errors)
              NZpercs = aggregate(melted$cnt,by=list(melted$cond),FUN=function(x) { sum(x>0)/length(x) })
              if (max(NZpercs$x)<0.15) { return(c(pval=1,status="low saturation (<15%) across all conditions (pan-growth-defect) - not analyzed")) }

              sums = aggregate(melted$cnt,by=list(melted$cond),FUN=sum)
              # to avoid model failing due to singular condition, add fake counts of 1 to all conds if any cond is all 0s
              if (0 %in% sums[,2]) {
                # print("adding pseudocounts")
                for (i in 1:length(sums[,1])) {
                  subset = melted[melted$cond==sums[i,1],]
                  newvec = subset[1,]
                  newvec$cnt = 1 # note: NZmean and NZperc are copied from last dataset in condition
                  #newvec$cnt = as.integer(mean(subset$cnt))+1 # add the mean for each condition as a pseudocount
                  melted = rbind(melted,newvec) }
              }
              status = "-"
              minCount = min(melted$cnt)
              f1 = ""
              mod1 = tryCatch(
                {
                  if (minCount == 0) {
                    f1 = zinbMod1
                    mod = zeroinfl(as.formula(zinbMod1),data=melted,dist="negbin")
                    coeffs = summary(mod)$coefficients
                    # [,1] is col of parms, [,2] is col of stderrs, assume Intercept is always first
                    #if (coeffs$count[,2][1]>0.5) { status = 'warning: high stderr on Intercept for mod1' }
                    mod
                  } else {
                    f1 = nbMod1
                    glm.nb(as.formula(nbMod1),data=melted)
                  }
                },
                error=function(err) {
                  status <<- err$message
                  return(NULL)
                })
              f0 = ""
              mod0 = tryCatch( # null model, independent of conditions
                {
                  if (minCount == 0) {
                    f0 = zinbMod0
                    mod = zeroinfl(as.formula(zinbMod0),data=melted,dist="negbin")
                    coeffs = summary(mod)$coefficients
                    # [,1] is col of parms, [,2] is col of stderrs, assume Intercept is always first
                    #if (coeffs$count[,2][1]>0.5) { status = 'warning: high stderr on Intercept for mod0' }
                    mod
                  } else {
                    f0 = nbMod0
                    glm.nb(as.formula(nbMod0),data=melted)
                  }
                },
                error=function(err) {
                  status <<- err$message
                  return(NULL)
                })
              if (DEBUG) {
                  print("Model 1:")
                  print(f1)
                  print(summary(mod1))
                  print("Model 0:")
                  print(f0)
                  print(summary(mod0))
              }

              if (is.null(mod1) | is.null(mod0)) { return (c(1, paste0("Model Error. ", status))) }
              if ((minCount == 0) && (sum(is.na(coef(summary(mod1))$count[,4]))>0)) { return(c(1, "Has Coefs, but Pvals are NAs (model failure)")) } # rare failure mode - has coefs, but pvals are NA
              df1 = attr(logLik(mod1),"df"); df0 = attr(logLik(mod0),"df") # should be (2*ngroups+1)-3
              if (DEBUG) print(sprintf("delta_log_likelihood=%f",logLik(mod1)-logLik(mod0)))
              pval = pchisq(2*(logLik(mod1)-logLik(mod0)),df=df1-df0,lower.tail=F) # alternatively, could use lrtest()
              # this gives same answer, but I would need to extract the Pvalue...
              #require(lmtest)
              #print(lrtest(mod1,mod0))
              return (c(pval, status))
            }
        ''')

        return globalenv['zinb_signif']

    def winsorize(self, data):
        unique_counts = numpy.unique(numpy.concatenate(data))
        if (len(unique_counts) < 2):
            return data
        else:
            n, n_minus_1 = unique_counts[heapq.nlargest(2, range(len(unique_counts)), unique_counts.take)]
            result = [[ n_minus_1 if count == n else count
                        for count in wig] for wig in data]
        return numpy.array(result)

    def is_number(self, s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    def run_zinb(self, data, genes, NZMeanByRep, LogZPercByRep, RvSiteindexesMap, conditions, covariates, interactions):
        """
            Runs Zinb for each gene across conditions and returns p and q values
            ([[Wigdata]], [Gene], [Number], [Number], {Rv: [SiteIndex]}, [Condition], [Covar], [Interaction]) -> Tuple([Number], [Number], [Status])
            Wigdata :: [Number]
            Gene :: {start, end, rv, gene, strand}
            SiteIndex: Integer
            Condition :: String
            Covar :: String
            Interaction :: String
            Status :: String
        """

        count = 0
        self.progress_range(len(genes))
        pvals,Rvs, status = [],[], []
        r_zinb_signif = self.def_r_zinb_signif()
        if (self.winz):
            self.transit_message("Winsorizing and running analysis...")

        self.transit_message("Condition: %s" % self.condition)

        comp1a = "1+cond"
        comp1b = "1+cond"

        # include cond in mod0 only if testing interactions
        comp0a = "1" if len(self.interactions)==0 else "1+cond"
        comp0b = "1" if len(self.interactions)==0 else "1+cond"
        for I in self.interactions: comp1a += "*"+I; comp1b += "*"+I; comp0a += "+"+I; comp0b += "+"+I
        for C in self.covars: comp1a += "+"+C; comp1b += "+"+C; comp0a += "+"+C; comp0b += "+"+C
        zinbMod1 = "cnt~%s+offset(log(NZmean))|%s+offset(logitZperc)" % (comp1a,comp1b)
        zinbMod0 = "cnt~%s+offset(log(NZmean))|%s+offset(logitZperc)" % (comp0a,comp0b)

        nbMod1 = "cnt~%s" % (comp1a)
        nbMod0 = "cnt~%s" % (comp0a)
        toRFloatOrStrVec = lambda xs: FloatVector([float(x) for x in xs]) if self.is_number(xs[0]) else StrVector(xs)

        for gene in genes:
            count += 1
            Rv = gene["rv"]
            ## Single gene case for debugging
            if (GENE):
                Rv = None
                if GENE in RvSiteindexesMap:
                    Rv = GENE
                else:
                    for g in genes:
                        if (g['gene'] == GENE):
                            Rv = g["rv"]
                            break
                if not Rv:
                    self.transit_error("Cannot find gene: {0}".format(GENE))
                    sys.exit(0)

            if (DEBUG):
               self.transit_message("======================================================================")
               self.transit_message(gene["rv"]+" "+gene["gene"])

            if (len(RvSiteindexesMap[Rv]) <= 1):
                status.append("TA sites <= 1, not analyzed")
                pvals.append(1)
            else:
                # For winsorization
                # norm_data = self.winsorize((map(
                #     lambda wigData: wigData[RvSiteindexesMap[Rv]], data))) if self.winz else list(map(lambda wigData: wigData[RvSiteindexesMap[Rv]], data))
                norm_data = list(map(lambda wigData: wigData[RvSiteindexesMap[Rv]], data))
                ([ readCounts,
                   condition,
                   covarsData,
                   interactionsData,
                   NZmean,
                   logitZPerc]) = self.melt_data(
                           norm_data,
                           conditions, covariates, interactions, NZMeanByRep, LogZPercByRep)
                if (numpy.sum(readCounts) == 0):
                    status.append("pan-essential (no counts in all conditions) - not analyzed")
                    pvals.append(1)
                else:
                    df_args = {
                        'cnt': IntVector(readCounts),
                        'cond': toRFloatOrStrVec(condition),
                        'NZmean': FloatVector(NZmean),
                        'logitZperc': FloatVector(logitZPerc)
                        }
                    ## Add columns for covariates and interactions if they exist.
                    df_args.update(list(map(lambda t_ic: (t_ic[1], toRFloatOrStrVec(covarsData[t_ic[0]])), enumerate(self.covars))))
                    df_args.update(list(map(lambda t_ic: (t_ic[1], toRFloatOrStrVec(interactionsData[t_ic[0]])), enumerate(self.interactions))))

                    melted = DataFrame(df_args)
                    # r_args = [IntVector(readCounts), StrVector(condition), melted, map(lambda x: StrVector(x), covars), FloatVector(NZmean), FloatVector(logitZPerc)] + [True]
                    debugFlag = True if DEBUG or GENE else False
                    pval, msg = r_zinb_signif(melted, zinbMod1, zinbMod0, nbMod1, nbMod0, debugFlag)
                    status.append(msg)
                    pvals.append(float(pval))
                if (DEBUG or GENE):
                    self.transit_message("Pval for Gene {0}: {1}, status: {2}".format(Rv, pvals[-1], status[-1]))
                if (GENE):
                    self.transit_message("Ran for single gene. Exiting...")
                    sys.exit(0)
            Rvs.append(Rv)
            # Update progress
            text = "Running ZINB Method... %5.1f%%" % (100.0*count/len(genes))
            self.progress_update(text, count)

        pvals = numpy.array(pvals)
        mask = numpy.isfinite(pvals)
        qvals = numpy.full(pvals.shape, numpy.nan)
        qvals[mask] = statsmodels.stats.multitest.fdrcorrection(pvals)[1] # BH, alpha=0.05

        p,q,statusMap = {},{},{}
        for i,rv in enumerate(Rvs):
            p[rv],q[rv],statusMap[rv] = pvals[i],qvals[i],status[i]
        return (p, q, statusMap)

    # from {key->value} return {value->[keys]}
    def invertDict(self,d):
      e = {}
      for k,v in d.items():
         if v not in e: e[v] = []
         e[v].append(k)
      return e 

    # pairs is a list of (var,val); samples is a set; varsByFileList is a list of dictionaries mapping values to samples for each var (parallel to vars)
    # recursive: keep calling till vars reduced to empty

    def expandVar(self,pairs,vars,varsByFileList,vars2vals,samples):
      if len(vars)==0:
        s = "%s=%s" % (pairs[0][0],pairs[0][1])
        for i in range(1,len(pairs)): s += " & %s=%s" % (pairs[i][0],pairs[i][1])
        s += ": %s" % len(samples)
        print(s)
        if len(samples)==0: return True
      else:
        var,valsDict = vars[0],varsByFileList[0]
        inv = self.invertDict(valsDict)
        any_empty = False
        for val in vars2vals[var]:
          subset = samples.intersection(set(inv[val]))
          res = self.expandVar(pairs+[(var,val)],vars[1:],varsByFileList[1:],vars2vals,subset)
          any_empty = any_empty or res
        return any_empty

    def Run(self):
        self.transit_message("Starting ZINB analysis")
        start_time = time.time()
        packnames = ("MASS", "pscl")
        r_packages_needed = [x for x in packnames if not rpackages.isinstalled(x)]
        if (len(r_packages_needed) > 0):
            self.transit_error(
                    "Error: Following R packages are required: %(0)s. From R console, You can install them using install.packages(c(%(0)s))"
                    % ({'0': '"{0}"'.format('", "'.join(r_packages_needed))}))
            sys.exit(1)


        self.transit_message("Getting Data")
        (sites, data, filenamesInCombWig) = tnseq_tools.read_combined_wig(self.combined_wig)

        self.transit_message("Normalizing using: %s" % self.normalization)
        (data, factors) = norm_tools.normalize_data(data, self.normalization)

        condition_name = self.condition
        # if a covar is not found, this crashes; check for it?
        conditionsByFile, covariatesByFileList, interactionsByFileList, orderingMetadata = tnseq_tools.read_samples_metadata(self.metadata, self.covars, self.interactions, condition_name=condition_name)

        ## [Condition] in the order of files in combined wig
        conditions = self.wigs_to_conditions(
            conditionsByFile,
            filenamesInCombWig)
        ## [Covariate] in the order of files in combined wig
        covariates = self.wigs_to_covariates(
            covariatesByFileList,
            filenamesInCombWig)
        ## [Interaction] in the order of files in combined wig
        interactions = self.wigs_to_interactions(
            interactionsByFileList,
            filenamesInCombWig)

        conditionsList = self.select_conditions(conditions,self.included_conditions,self.ignored_conditions,orderingMetadata)
        data, conditions, covariates, interactions = self.filter_wigs_by_conditions2(
                data,
                conditions,
                conditionsList,
                covariates = covariates,
                interactions = interactions)

        # show the samples associated with each condition (and covariates or interactions, if defined), and count samples in each cross-product of vars

        filesByCondition  = self.invertDict(conditionsByFile)
        samples_used = set()
        for cond in conditionsList: samples_used.update(filesByCondition[cond])
        vars = [condition_name]+self.covars+self.interactions
        vars2vals = {}
        vars2vals[condition_name] = list(set(conditions))
        for i,var in enumerate(self.covars): vars2vals[var] = list(set(covariates[i]))
        for i,var in enumerate(self.interactions): vars2vals[var] = list(set(interactions[i]))
        varsByFileList = [conditionsByFile]+covariatesByFileList+interactionsByFileList
        for i,var in enumerate(vars):
          print("\nCondition/Covariate/Interaction: %s" % vars[i])
          filesByVar = self.invertDict(varsByFileList[i])
          for k,v in filesByVar.items():
            samples = list(samples_used.intersection(set(v)))
            if k in vars2vals.get(var,[]): print("%s: %s" % (k,' '.join(samples))) 
        pairs = []
        print("\nsamples in cross-product:")
        any_empty = self.expandVar([],vars,varsByFileList,vars2vals,set(samples_used))
        if any_empty: print("warning: ZINB requires samples in all combinations of conditions; the fact that one is empty could result in Model Errors")

        genes = tnseq_tools.read_genes(self.annotation_path)

        TASiteindexMap = {TA: i for i, TA in enumerate(sites)}
        RvSiteindexesMap = tnseq_tools.rv_siteindexes_map(genes, TASiteindexMap, nterm=self.NTerminus, cterm=self.CTerminus)
        statsByRv, statGroupNames = self.stats_by_rv(data, RvSiteindexesMap, genes, conditions, interactions)
        LogZPercByRep, NZMeanByRep = self.global_stats_for_rep(data)

        self.transit_message("Running ZINB")
        pvals, qvals, run_status = self.run_zinb(data, genes, NZMeanByRep, LogZPercByRep, RvSiteindexesMap, conditions, covariates, interactions)

        def orderStats(x, y):
            ic1 = x.split(SEPARATOR)
            ic2 = y.split(SEPARATOR)
            c1, i1 = (ic1[0], ic1[1]) if len(ic1) > 1 else (ic1[0], None)
            c2, i2 = (ic2[0], ic2[1]) if len(ic2) > 1 else (ic2[0], None)

            if len(self.included_conditions) > 0:
                condDiff = (self.included_conditions.index(c1) - self.included_conditions.index(c2))
                ## Order by interaction, if stat belongs to same condition
                if condDiff == 0 and i1 is not None and i2 is not None:
                    return (orderingMetadata['interaction'].index(i1) - orderingMetadata['interaction'].index(i2))
                return condDiff

            ## Order by samples metadata, if include flag not provided.
            condDiff = (orderingMetadata['condition'].index(c1) - orderingMetadata['condition'].index(c2))
            if condDiff == 0 and i1 is not None and i2 is not None:
                return (orderingMetadata['interaction'].index(i1) - orderingMetadata['interaction'].index(i2))
            return condDiff

        orderedStatGroupNames = sorted(statGroupNames, key=functools.cmp_to_key(orderStats))
        headersStatGroupNames = [x.replace(SEPARATOR,'_') for x in orderedStatGroupNames]

        self.transit_message("Adding File: %s" % (self.output))
        file = open(self.output,"w")
        if len(headersStatGroupNames)==2: lfcNames = ["LFC"] 
        else: lfcNames = list(map(lambda v: "LFC_"+v,headersStatGroupNames))
        head = ("Rv Gene TAs".split() +
                list(map(lambda v: "Mean_" + v, headersStatGroupNames)) +
                lfcNames+
                list(map(lambda v: "NZmean_" + v, headersStatGroupNames)) +
                list(map(lambda v: "NZperc_" + v, headersStatGroupNames)) +
                "pval padj".split() + ["status"])

        file.write("#Console: python3 %s\n" % " ".join(sys.argv))
        file.write('\t'.join(head)+EOL)
        for gene in genes:
            Rv = gene["rv"]
            means = [statsByRv[Rv]['mean'][group] for group in orderedStatGroupNames]
            PC = 5
            if len(means)==2: LFCs = [numpy.math.log((means[1]+PC)/(means[0]+PC),2)]
            else: 
              m = numpy.mean(means)
              LFCs = [numpy.math.log((x+PC)/(m+PC),2) for x in means]
            vals = ([Rv, gene["gene"], str(len(RvSiteindexesMap[Rv]))] +
                    ["%0.1f" % statsByRv[Rv]['mean'][group] for group in orderedStatGroupNames] +
                    ["%0.3f" % x for x in LFCs]+
                    ["%0.1f" % statsByRv[Rv]['nz_mean'][group] for group in orderedStatGroupNames] +
                    ["%0.2f" % statsByRv[Rv]['nz_perc'][group] for group in orderedStatGroupNames] +
                    ["%f" % x for x in [pvals[Rv], qvals[Rv]]]) + [run_status[Rv]]
            file.write('\t'.join(vals)+EOL)
        file.close()
        self.transit_message("Finished Zinb analysis")
        self.transit_message("Time: %0.1fs\n" % (time.time() - start_time))

    @classmethod
    def usage_string(self):
        return """python3 %s zinb <combined wig file> <samples_metadata file> <annotation .prot_table> <output file> [Optional Arguments]

        Optional Arguments:
        -n <string>         :=  Normalization method. Default: -n TTR
        --ignore-conditions <cond1,cond2> :=  Comma separated list of conditions to ignore, for the analysis.
        --include-conditions <cond1,cond2> :=  Comma separated list of conditions to include, for the analysis. Conditions not in this list, will be ignored.
        -iN <float>     :=  Ignore TAs occuring within given percentage (as integer) of the N terminus. Default: -iN 5
        -iC <float>     :=  Ignore TAs occuring within given percentage (as integer) of the C terminus. Default: -iC 5
        --condition     :=  columnname (in samples_metadata) to use as the Condition. Default: "Condition"
        --covars <covar1,covar2...>     :=  Comma separated list of covariates (in metadata file) to include, for the analysis.
        --interactions <covar1,covar2...>     :=  Comma separated list of covariates to include, that interact with the condition for the analysis. Must be factors
        --gene <RV number or Gene name> := Run method for one gene and print model output.

        """ % (sys.argv[0])

if __name__ == "__main__":
    main()

