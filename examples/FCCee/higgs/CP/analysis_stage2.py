import os, copy # tagging
import ROOT

#Mandatory: List of processes
processList = {
    'wzp6_ee_nunuH_Htautau_ecm240': {'chunks':10}, #check that it's fine to keep them in chunks, otherwise just remove the option and leave {},
    'wzp6_ee_nunuH_Hbb_ecm240': {'chunks':10},
    'wzp6_ee_nunuH_Hcc_ecm240': {'chunks':10},
    'wzp6_ee_nunuH_Huu_ecm240': {'chunks':10},
    'wzp6_ee_nunuH_Hdd_ecm240': {'chunks':10},
    'wzp6_ee_nunuH_Hss_ecm240': {'chunks':10},
    'wzp6_ee_nunuH_Hmumu_ecm240': {'chunks':10},
}

inputDir = "/eos/user/s/sgiappic/HiggsCP/stage1/test/"

#Optional: output directory, default is local running directory
outputDir   = "stage2" #your output directory

#Optional: ncpus, default is 4
nCPUS = 10

### necessary to run on HTCondor ###
eosType = "eosuser"

#Optional running on HTCondor, default is False
runBatch = False

#Optional batch queue name when running on HTCondor, default is workday
batchQueue = "microcentury"

#Optional computing account when running on HTCondor, default is group_u_FCC.local_gen
compGroup = "group_u_FCC.local_gen"

#Mandatory: RDFanalysis class where the use defines the operations on the TTree
class RDFanalysis():
    def analysers(df):

            df2 = (df

            ### to find already made functions, this is where they are or where they can be added instead of writing them here
            ### https://github.com/Edler1/FCCAnalyses-1/tree/7f6006a1e4579c9bc01a149732ea39685cbad951/analyzers/dataframe/src

            #################
            # Gen particles #
            #################

            # filter events based on gen or reco variables
            .Filter("n_FSRGenTau==2 && n_GenZ>0")
            
            .Define("FSRGenTau_Lxyz", "return sqrt(FSRGenTau_vertex_x.at(0)*FSRGenTau_vertex_x.at(0) + FSRGenTau_vertex_y.at(0)*FSRGenTau_vertex_y.at(0) + FSRGenTau_vertex_z.at(0)*FSRGenTau_vertex_z.at(0))") #in mm
    
            # tautau invariant mass
            .Define("GenDiTau_e", "if (n_FSRGenTau>1) return (FSRGenTau_e.at(0) + FSRGenTau_e.at(1)); else return float(-1.);")
            .Define("GenDiTau_px", "if (n_FSRGenTau>1) return (FSRGenTau_px.at(0) + FSRGenTau_px.at(1)); else return float(-1.);")
            .Define("GenDiTau_py", "if (n_FSRGenTau>1) return (FSRGenTau_py.at(0) + FSRGenTau_py.at(1)); else return float(-1.);")
            .Define("GenDiTau_pz", "if (n_FSRGenTau>1) return (FSRGenTau_pz.at(0) + FSRGenTau_pz.at(1)); else return float(-1.);")
            .Define("GenDiTau_invMass", "if (n_FSRGenTau>1) return sqrt(GenDiTau_e*GenDiTau_e - GenDiTau_px*GenDiTau_px - GenDiTau_py*GenDiTau_py - GenDiTau_pz*GenDiTau_pz ); else return float(-1.);")
            
            # cosine between two leptons, in lab frame
            .Define("GenDiTau_p", "if (n_FSRGenTau>1) return sqrt(GenDiTau_px*GenDiTau_px + GenDiTau_py*GenDiTau_py + GenDiTau_pz*GenDiTau_pz); else return float(-1.);")
            .Define("GenDiTau_scalar", "if (n_FSRGenTau>1) return (FSRGenTau_px.at(0)*FSRGenTau_px.at(1) + FSRGenTau_py.at(0)*FSRGenTau_py.at(1) + FSRGenTau_pz.at(0)*FSRGenTau_pz.at(1)); else return float(-1.);")
            .Define("GenDiTau_cos", "if (n_FSRGenTau>1) return (GenDiTau_scalar/(FSRGenTau_p.at(0)*FSRGenTau_p.at(1))); else return float(-2.);")

            # angular distance between two leptons, in lab frame
            # deltaEta and deltaPhi return the absolute values of the difference, may be intersting to keep the sign and order the taus by rapidity (y) (DOI: 10.1103/PhysRevD.99.095007) or soemthing else (pt...)
            .Define("GenDiTau_absDEta","if (n_FSRGenTau>1) return myUtils::deltaEta(FSRGenTau_eta.at(0), FSRGenTau_eta.at(1)); else return float(-10.);")
            .Define("GenDiTau_absDPhi","if (n_FSRGenTau>1) return myUtils::deltaPhi(FSRGenTau_phi.at(0), FSRGenTau_phi.at(1)); else return float(-10.);")
            .Define("GenDiTau_DEta","if (n_FSRGenTau>1 && FSRGenTau_y.at(0)>FSRGenTau_y.at(1)) return FSRGenTau_eta.at(0) - FSRGenTau_eta.at(1); \
                                    else if (n_FSRGenTau>1 && FSRGenTau_y.at(0)<FSRGenTau_y.at(1)) return FSRGenTau_eta.at(1) - FSRGenTau_eta.at(0); else return float(-10.);")
            .Define("GenDiTau_DPhi","if (n_FSRGenTau>1 && FSRGenTau_y.at(0)>FSRGenTau_y.at(1)) return FSRGenTau_phi.at(0) - FSRGenTau_phi.at(1); \
                                    else if (n_FSRGenTau>1 && FSRGenTau_y.at(0)<FSRGenTau_y.at(1)) return FSRGenTau_phi.at(1) - FSRGenTau_phi.at(0); else return float(-10.);")
            .Define("GenDiTau_DR","if (n_FSRGenTau>1) return myUtils::deltaR(FSRGenTau_phi.at(0), FSRGenTau_phi.at(1), FSRGenTau_eta.at(0), FSRGenTau_eta.at(1)); else return float(-1.);")

            #.Define("GenHiggs_e",      "return FSRGenTau_e.at(0) + FSRGenTau_e.at(1)")
            #.Define("GenHiggs_px",      "return FSRGenTau_px.at(0) + FSRGenTau_px.at(1)") #components have the right sign assigned to them already
            #.Define("GenHiggs_py",      "return FSRGenTau_py.at(0) + FSRGenTau_py.at(1)")
            #.Define("GenHiggs_pz",      "return FSRGenTau_pz.at(0) + FSRGenTau_pz.at(1)")
            #.Define("GenHiggs_p",      "return sqrt(GenHiggs_px*GenHiggs_px + GenHiggs_py*GenHiggs_py + GenHiggs_pz*GenHiggs_pz)")
            .Define("GenHiggs_p4",      "if (n_FSRGenTau>1) return myUtils::build_p4(FSRGenTau_px.at(0) + FSRGenTau_px.at(1), FSRGenTau_py.at(0) + FSRGenTau_py.at(1), FSRGenTau_pz.at(0) + FSRGenTau_pz.at(1), FSRGenTau_e.at(0) + FSRGenTau_e.at(1)); else return ROOT::VecOps::RVec<TLorentzVector>{}")
            .Define("GenHiggs_gamma",  "myUtils::get_gamma(GenHiggs_p, GenHiggs_e)") # momentum then energy

            #.Define("GenHiggsTauPlus_scalar",  "if (n_FSRGenTau>1 && FSRGenTau_charge==1) return FSRGenTau_px*GenHiggs_px + FSRGenTau_py*GenHiggs_py + FSRGenTau_pz*GenHiggs_pz; else return float(-1.)")
            #.Define("HiggsRF_GenTauPlus_px",    "if (n_FSRGenTau>1 && FSRGenTau_charge==1) return FSRGenTau_px + (GenHiggs_gamma -1)*GenHiggsTauPlus_scalar*GenHiggs_px/(GenHiggs_p*GenHiggs_p) - GenHiggs_gamma*FSRGenTau_e*GenHiggs_px")
            #.Define("HiggsRF_GenTauPlus_py",    "if (n_FSRGenTau>1 && FSRGenTau_charge==1) return FSRGenTau_py + (GenHiggs_gamma -1)*GenHiggsTauPlus_scalar*GenHiggs_py/(GenHiggs_p*GenHiggs_p) - GenHiggs_gamma*FSRGenTau_e*GenHiggs_py")
            #.Define("HiggsRF_GenTauPlus_pz",    "if (n_FSRGenTau>1 && FSRGenTau_charge==1) return FSRGenTau_pz + (GenHiggs_gamma -1)*GenHiggsTauPlus_scalar*GenHiggs_pz/(GenHiggs_p*GenHiggs_p) - GenHiggs_gamma*FSRGenTau_e*GenHiggs_pz")
            #.Define("HiggsFR_GenTauPlus_pt",    "if (n_FSRGenTau>1 && FSRGenTau_charge==1) return sqrt(HiggsRF_GenTauPlus_px*HiggsRF_GenTauPlus_px + HiggsRF_GenTauPlus_py*HiggsRF_GenTauPlus_py)")
            #.Define("HiggsFR_GenTauPlus_pyz",    "if (n_FSRGenTau>1 && FSRGenTau_charge==1) return sqrt(HiggsRF_GenTauPlus_px*HiggsRF_GenTauPlus_px + HiggsRF_GenTauPlus_py*HiggsRF_GenTauPlus_py)")
            #.Define("HiggsRF_GenTauPlus_phi",      "if (n_FSRGenTau>1 && FSRGenTau_charge==1) return arccos(HiggsRF_GenTauPlus_px/HiggsRF_GenTauPlus_pt)")
            #.Define("HiggsRF_GenTauPlus_eta",      "if (n_FSRGenTau>1 && FSRGenTau_charge==1) return arccos(HiggsRF_GenTauPlus_px/HiggsRF_GenTauPlus_pt)")
            
            .Define("FSRGenTauPlus_p4",     "if (FSRGenTau_charge==1) return myUtils::build_p4(FSRGenTau_px, FSRGenTau_pz, FSRGenTau_e); else return ROOT::VecOps::RVec<TLorentzVector>{} ")
            .Define("GenHiggsTauPlus_scalar",  "myUtils::get_scalar(FSRGenTauPlus_p4, GenHiggs_p4)")
            .Define("HiggRF_GenTauPlus_p4",     "myUtils::boosted_p4(GenHiggs_p4, FSRGenTauPlus_p4, GenHiggs_gamma)")
            .Define("HiggsRF_GenTauPlus_px",    "myUtils::get_pxtvl(HiggsRF_GenTauPlus_p4)")
            .Define("HiggsRF_GenTauPlus_py",    "myUtils::get_pytvl(HiggsRF_GenTauPlus_p4)")
            .Define("HiggsRF_GenTauPlus_pz",    "myUtils::get_pxtvl(HiggsRF_GenTauPlus_p4)")
            .Define("HiggsRF_GenTauPlus_p",    "myUtils::get_ptvl(HiggsRF_GenTauPlus_p4)")
            .Define("HiggsRF_GenTauPlus_pt",    "myUtils::get_pttvl(HiggsRF_GenTauPlus_p4)")
            .Define("HiggsRF_GenTauPlus_e",    "myUtils::get_etvl(HiggsRF_GenTauPlus_p4)")
            .Define("HiggsRF_GenTauPlus_eta",    "myUtils::get_etatvl(HiggsRF_GenTauPlus_p4)")
            .Define("HiggsRF_GenTauPlus_phi",    "myUtils::get_phitvl(HiggsRF_GenTauPlus_p4)")
            .Define("HiggsRF_GenTauPlus_theta",    "myUtils::get_thetatvl(HiggsRF_GenTauPlus_p4)")
            .Define("HiggsRF_GenTauPlus_y",    "myUtils::get_ytvl(HiggsRF_GenTauPlus_p4)")

            #.Define("FSRGenTauMin_p4",     "if (FSRGenTau_charge==-1) return myUtils::build_p4(FSRGenTau_px, FSRGenTau_pz, FSRGenTau_e); else return ROOT::VecOps::RVec<TLorentzVector>{}")
            #.Define("GenHiggsTauMin_scalar",  "if (n_FSRGenTau>1 && FSRGenTau_charge==-1) return FSRGenTau_px*GenHiggs_px + FSRGenTau_py*GenHiggs_py + FSRGenTau_pz*GenHiggs_pz")
            #.Define("HiggsRF_GenTauMin_px",    "if (n_FSRGenTau>1 && FSRGenTau_charge==-1) return FSRGenTau_px + (GenHiggs_gamma -1)*GenHiggsTauMin_scalar*GenHiggs_px/(GenHiggs_p*GenHiggs_p) - GenHiggs_gamma*FSRGenTau_e*GenHiggs_px")
            #.Define("HiggsRF_GenTauMin_py",    "if (n_FSRGenTau>1 && FSRGenTau_charge==-1) return FSRGenTau_py + (GenHiggs_gamma -1)*GenHiggsTauMin_scalar*GenHiggs_py/(GenHiggs_p*GenHiggs_p) - GenHiggs_gamma*FSRGenTau_e*GenHiggs_py")
            #.Define("HiggsRF_GenTauMin_pz",    "if (n_FSRGenTau>1 && FSRGenTau_charge==-1) return FSRGenTau_pz + (GenHiggs_gamma -1)*GenHiggsTauMin_scalar*GenHiggs_pz/(GenHiggs_p*GenHiggs_p) - GenHiggs_gamma*FSRGenTau_e*GenHiggs_pz")

            .Define("FSRGenTauMin_p4",     "if (FSRGenTau_charge==-1) return myUtils::build_p4(FSRGenTau_px, FSRGenTau_pz, FSRGenTau_e); else return ROOT::VecOps::RVec<TLorentzVector>{} ")
            .Define("GenHiggsTauMin_scalar",  "myUtils::get_scalar(FSRGenTauMin_p4, GenHiggs_p4)")
            .Define("HiggRF_GenTauMin_p4",     "myUtils::boosted_p4(GenHiggs_p4, FSRGenTauMin_p4, GenHiggs_gamma)")
            .Define("HiggsRF_GenTauMin_px",    "myUtils::get_pxtvl(HiggsRF_GenTauMin_p4)")
            .Define("HiggsRF_GenTauMin_py",    "myUtils::get_pytvl(HiggsRF_GenTauMin_p4)")
            .Define("HiggsRF_GenTauMin_pz",    "myUtils::get_pxtvl(HiggsRF_GenTauMin_p4)")
            .Define("HiggsRF_GenTauMin_p",    "myUtils::get_ptvl(HiggsRF_GenTauMin_p4)")
            .Define("HiggsRF_GenTauMin_pt",    "myUtils::get_pttvl(HiggsRF_GenTauMin_p4)")
            .Define("HiggsRF_GenTauMin_e",    "myUtils::get_etvl(HiggsRF_GenTauMin_p4)")
            .Define("HiggsRF_GenTauMin_eta",    "myUtils::get_etatvl(HiggsRF_GenTauMin_p4)")
            .Define("HiggsRF_GenTauMin_phi",    "myUtils::get_phitvl(HiggsRF_GenTauMin_p4)")
            .Define("HiggsRF_GenTauMin_theta",    "myUtils::get_thetatvl(HiggsRF_GenTauMin_p4)")
            .Define("HiggsRF_GenTauMin_y",    "myUtils::get_ytvl(HiggsRF_GenTauMin_p4)")

            .Define("HiggsRF_GenDiTau_DEta",    "if (HiggsRF_GenTauPlus_y>HiggsRF_GenTauMin_y) return HiggsRF_GenTauPlus_eta - HiggsRF_GenTauMin_eta; \
                                    else (HiggsRF_GenTauPlus_y<HiggsRF_GenTauMin_y) return HiggsRF_GenTauMin_eta - HiggsRF_GenTauPlu_eta;")
            .Define("HiggsRF_GenDiTau_DPhi",    "if (HiggsRF_GenTauPlus_y>HiggsRF_GenTauMin_y) return HiggsRF_GenTauPlus_phi - HiggsRF_GenTauMin_phi; \
                                    else (HiggsRF_GenTauPlus_y<HiggsRF_GenTauMin_y) return HiggsRF_GenTauMin_phi - HiggsRF_GenTauPlu_phi;")

            ##################
            # Reco particles #
            ##################

            


            #############################################
            ##        Build Tau -> 3Pi candidates      ##
            #############################################

            .Define("Tau23PiCandidates",         "myUtils::build_tau23pi(VertexObject,RecoPartPIDAtVertex)")
            .Define("n_Tau23PiCandidates",        "float(myUtils::getFCCAnalysesComposite_N(Tau23PiCandidates))")

            .Define("Tau23PiCandidates_mass",    "myUtils::getFCCAnalysesComposite_mass(Tau23PiCandidates)")
            .Define("Tau23PiCandidates_q",       "myUtils::getFCCAnalysesComposite_charge(Tau23PiCandidates)")
            .Define("Tau23PiCandidates_px",      "myUtils::getFCCAnalysesComposite_p(Tau23PiCandidates,0)")
            .Define("Tau23PiCandidates_py",      "myUtils::getFCCAnalysesComposite_p(Tau23PiCandidates,1)")
            .Define("Tau23PiCandidates_pz",      "myUtils::getFCCAnalysesComposite_p(Tau23PiCandidates,2)")
            .Define("Tau23PiCandidates_p",       "myUtils::getFCCAnalysesComposite_p(Tau23PiCandidates,-1)")
            .Define("Tau23PiCandidates_B",       "myUtils::getFCCAnalysesComposite_B(Tau23PiCandidates, VertexObject, RecoPartPIDAtVertex)")
            .Define("Tau23PiCandidates_track",   "myUtils::getFCCAnalysesComposite_track(Tau23PiCandidates, VertexObject)")
            .Define("Tau23PiCandidates_d0",      "myUtils::get_trackd0(Tau23PiCandidates_track)")
            .Define("Tau23PiCandidates_z0",      "myUtils::get_trackz0(Tau23PiCandidates_track)")

            .Define("Tau23PiCandidates_pion1px", "myUtils::getFCCAnalysesComposite_p(Tau23PiCandidates, VertexObject, RecoPartPIDAtVertex, 0, 0)")
            .Define("Tau23PiCandidates_pion1py", "myUtils::getFCCAnalysesComposite_p(Tau23PiCandidates, VertexObject, RecoPartPIDAtVertex, 0, 1)")
            .Define("Tau23PiCandidates_pion1pz", "myUtils::getFCCAnalysesComposite_p(Tau23PiCandidates, VertexObject, RecoPartPIDAtVertex, 0, 2)")
            .Define("Tau23PiCandidates_pion1p",  "myUtils::getFCCAnalysesComposite_p(Tau23PiCandidates, VertexObject, RecoPartPIDAtVertex, 0, -1)")
            .Define("Tau23PiCandidates_pion1q",  "myUtils::getFCCAnalysesComposite_q(Tau23PiCandidates, VertexObject, RecoPartPIDAtVertex, 0)")
            .Define("Tau23PiCandidates_pion1d0", "myUtils::getFCCAnalysesComposite_d0(Tau23PiCandidates, VertexObject, 0)")
            .Define("Tau23PiCandidates_pion1z0", "myUtils::getFCCAnalysesComposite_z0(Tau23PiCandidates, VertexObject, 0)")

            .Define("Tau23PiCandidates_pion2px", "myUtils::getFCCAnalysesComposite_p(Tau23PiCandidates, VertexObject, RecoPartPIDAtVertex, 1, 0)")
            .Define("Tau23PiCandidates_pion2py", "myUtils::getFCCAnalysesComposite_p(Tau23PiCandidates, VertexObject, RecoPartPIDAtVertex, 1, 1)")
            .Define("Tau23PiCandidates_pion2pz", "myUtils::getFCCAnalysesComposite_p(Tau23PiCandidates, VertexObject, RecoPartPIDAtVertex, 1, 2)")
            .Define("Tau23PiCandidates_pion2p",  "myUtils::getFCCAnalysesComposite_p(Tau23PiCandidates, VertexObject, RecoPartPIDAtVertex, 1, -1)")
            .Define("Tau23PiCandidates_pion2q",  "myUtils::getFCCAnalysesComposite_q(Tau23PiCandidates, VertexObject, RecoPartPIDAtVertex, 1)")
            .Define("Tau23PiCandidates_pion2d0", "myUtils::getFCCAnalysesComposite_d0(Tau23PiCandidates, VertexObject, 1)")
            .Define("Tau23PiCandidates_pion2z0", "myUtils::getFCCAnalysesComposite_z0(Tau23PiCandidates, VertexObject, 1)")

            .Define("Tau23PiCandidates_pion3px", "myUtils::getFCCAnalysesComposite_p(Tau23PiCandidates, VertexObject, RecoPartPIDAtVertex, 2, 0)")
            .Define("Tau23PiCandidates_pion3py", "myUtils::getFCCAnalysesComposite_p(Tau23PiCandidates, VertexObject, RecoPartPIDAtVertex, 2, 1)")
            .Define("Tau23PiCandidates_pion3pz", "myUtils::getFCCAnalysesComposite_p(Tau23PiCandidates, VertexObject, RecoPartPIDAtVertex, 2, 2)")
            .Define("Tau23PiCandidates_pion3p",  "myUtils::getFCCAnalysesComposite_p(Tau23PiCandidates, VertexObject, RecoPartPIDAtVertex, 2, -1)")
            .Define("Tau23PiCandidates_pion3q",  "myUtils::getFCCAnalysesComposite_q(Tau23PiCandidates, VertexObject, RecoPartPIDAtVertex, 2)")
            .Define("Tau23PiCandidates_pion3d0", "myUtils::getFCCAnalysesComposite_d0(Tau23PiCandidates, VertexObject, 2)")
            .Define("Tau23PiCandidates_pion3z0", "myUtils::getFCCAnalysesComposite_z0(Tau23PiCandidates, VertexObject, 2)")

        )
            return df2

    #__________________________________________________________
    #Mandatory: output function, please make sure you return the branchlist as a python list
    def output():
        branchList = [
                ######## Monte-Carlo particles #######
                "FSRGenTau_Lxyz",
                "GenDiTau_invMass",
                "GenDiTau_cos",
                "GenDiTau_DR",

                ######## Reconstructed particles #######
                "n_Tau23PiCandidates", "Tau23PiCandidates_mass", "Tau23PiCandidates_B",
                "Tau23PiCandidates_px", "Tau23PiCandidates_py", "Tau23PiCandidates_pz", "Tau23PiCandidates_p", "Tau23PiCandidates_q",
                "Tau23PiCandidates_d0",  "Tau23PiCandidates_z0",

                "Tau23PiCandidates_pion1px", "Tau23PiCandidates_pion1py", "Tau23PiCandidates_pion1pz",
                "Tau23PiCandidates_pion1p", "Tau23PiCandidates_pion1q", "Tau23PiCandidates_pion1d0", "Tau23PiCandidates_pion1z0",
                "Tau23PiCandidates_pion2px", "Tau23PiCandidates_pion2py", "Tau23PiCandidates_pion2pz",
                "Tau23PiCandidates_pion2p", "Tau23PiCandidates_pion2q", "Tau23PiCandidates_pion2d0", "Tau23PiCandidates_pion2z0",
                "Tau23PiCandidates_pion3px", "Tau23PiCandidates_pion3py", "Tau23PiCandidates_pion3pz",
                "Tau23PiCandidates_pion3p", "Tau23PiCandidates_pion3q", "Tau23PiCandidates_pion3d0", "Tau23PiCandidates_pion3z0",    
                    ]
        return branchList