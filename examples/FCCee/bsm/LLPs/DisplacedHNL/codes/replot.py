#code adapted from FCCAnalyses/do_plots.py

import sys
import os
import os.path
import ntpath
import importlib
import copy
import re
import logging
import ROOT

def sorted_dict_values(dic: dict) -> list:
    ''''
    Sort values in the dictionary.
    '''
    keys = sorted(dic)
    return [dic[key] for key in keys]

def make_dir_if_not_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Directory created successfully.")
    else:
        print(f"Directory already exists.")

DIRECTORY = '/eos/user/s/sgiappic/2HNL_gen/final/' 

CUTS = [
    #"sel2RecoSF_vetoes",
    "sel2Gen_vetoes",
    #"sel2RecoSF_vetoes_tracks_M80_p40_11.5MEpt_0.8cos",
    #"sel2RecoDF_vetoes_tracks_M80_7MEpt_0.8cos_0.04Lxy",
    #'sel2RecoSF_vetoes_tracks',
    #'sel2RecoDF_vetoes_tracks',
 ] 

LABELS = {
    "sel2RecoSF_vetoes_tracks_M80_p40_11.5MEpt_0.8cos":"SF selection, M(l,l)<80 GeV, p<40 GeV, p_{T,miss}>11.5 Gev, cos#theta>-0.8",
    "sel2RecoDF_vetoes_tracks_M80_7MEpt_0.8cos_0.04Lxy":"DF with 2 tracks, M(l,l)<80 GeV, p_{T,miss}>7 Gev, cos#theta>-0.8, L_{xyz}>0.04 mm",
    "sel2Reco_vetoes":"Two leptons, no photons, no jets",
    "sel2RecoSF_vetoes":"Two same flavor leptons, no photons, no jets",
    "sel2Gen_vetoes":"Two leptons, no photons, no jets"
 }

DIR_PLOTS = '/eos/user/s/sgiappic/2HNL_gen/plots/' 

ana_tex        = "e^{+}e^{-} #rightarrow N_{1,2} #nu, N_{1,2} #rightarrow ll#nu"
energy         = 91
collider       = 'FCC-ee'
intLumi        = 180 #ab-1

VARIABLES = [
    "Reco_DR",
]

VARIABLES_ALL = [
    
    #gen variables
    "n_FSGenElectron",
    "n_FSGenMuon",
    "n_FSGenLepton",
    "n_GenN",
    "n_FSGenPhoton",

    "FSGen_Lxy",
    "FSGen_Lxyz",
    "FSGen_Lxyz_prompt",
    "FSGen_invMass",

    "GenN_mass",
    "GenN_time",
    "GenN_tau",
    "GenN_txyz",
    "GenN_Lxyz_tau",
    "GenN_Lxyz_time",

    #reco variables
    "n_RecoTracks",
    "n_PrimaryTracks",
    "n_SecondaryTracks",
    "n_RecoDVs",
    "n_RecoJets",
    "n_RecoPhotons",
    "n_RecoElectrons",
    "n_RecoMuons",
    "n_RecoLeptons",

    "Reco_e",
    "Reco_p",
    "Reco_pt",
    "Reco_px",
    "Reco_py",
    "Reco_pz",
    "Reco_eta",
    "Reco_theta",
    "Reco_phi",

    "RecoTrack_absD0_prompt",
    "RecoTrack_absZ0_prompt",
    "RecoTrack_absD0_med",
    "RecoTrack_absZ0_med",
    "RecoTrack_absD0",
    "RecoTrack_absZ0",
    "RecoTrack_absD0sig",
    "RecoTrack_absD0sig_med",
    "RecoTrack_absD0sig_prompt",
    "RecoTrack_absZ0sig",
    "RecoTrack_absZ0sig_med",
    "RecoTrack_absZ0sig_prompt",
    "RecoTrack_D0cov",
    "RecoTrack_Z0cov",

    "Reco_DecayVertexLepton_x",       
    "Reco_DecayVertexLepton_y",          
    "Reco_DecayVertexLepton_z",          
    "Reco_DecayVertexLepton_x_prompt",   
    "Reco_DecayVertexLepton_y_prompt",    
    "Reco_DecayVertexLepton_z_prompt",    
    "Reco_DecayVertexLepton_chi2",    
    "Reco_DecayVertexLepton_probability", 

    "Reco_Lxy",
    "Reco_Lxy_prompt",
    "Reco_Lxyz",
    "Reco_Lxyz_prompt",
    "Reco_Lxyz_LCFI",
    "Reco_Lxyz_prompt_LCFI",
    
    "Reco_invMass",
    "Reco_cos",
    "Reco_DR",

    "RecoMissingEnergy_e",
    "RecoMissingEnergy_p",
    "RecoMissingEnergy_pt",
    "RecoMissingEnergy_px",
    "RecoMissingEnergy_py",
    "RecoMissingEnergy_pz",
    "RecoMissingEnergy_eta",
    "RecoMissingEnergy_theta",
    "RecoMissingEnergy_phi",

 ] 

backgrounds = [
    #'p8_ee_Zee_ecm91',
    #'p8_ee_Zmumu_ecm91',
    #'p8_ee_Ztautau_ecm91',
    #'p8_ee_Zbb_ecm91',
    #'p8_ee_Zcc_ecm91',
    #'p8_ee_Zud_ecm91',
    #'p8_ee_Zss_ecm91',
    #'emununu',
    #'tatanunu',
]

blegend = {
    'p8_ee_Zee_ecm91': 'Z #rightarrow ee',
    'p8_ee_Zmumu_ecm91': 'Z #rightarrow #mu#mu',
    'p8_ee_Ztautau_ecm91': 'Z #rightarrow #tau#tau',
    'p8_ee_Zbb_ecm91': 'Z #rightarrow bb',
    'p8_ee_Zcc_ecm91': 'Z #rightarrow cc',
    'p8_ee_Zud_ecm91': 'Z #rightarrow ud',
    'p8_ee_Zss_ecm91': 'Z #rightarrow ss',
    'emununu': 'e#mu#nu#nu',
    'tatanunu': '#tau#tau#nu#nu',
}

bcolors = {
    'p8_ee_Zee_ecm91': 29,
    'p8_ee_Zmumu_ecm91': 32,
    'p8_ee_Ztautau_ecm91': 34,
    'p8_ee_Zbb_ecm91': 48,
    'p8_ee_Zcc_ecm91': 44,
    'p8_ee_Zud_ecm91': 41,
    'p8_ee_Zss_ecm91': 20,
    'emununu': 40,
    'tatanunu': 38,
}

signals = [
    'HNL_4e-8_10gev',
    'HNL_2.86e-12_30gev',
    'HNL_2.86e-7_30gev',
    #'HNL_5e-12_50gev',
    #'HNL_4e-10_80gev',
    'HNL_6.67e-8_60gev',
    'HNL_2.86e-8_80gev',
]

slegend = {
    'HNL_2.86e-12_30gev': 'U^{2}=2.86e-12, M_{N}=30 GeV',
    'HNL_2.86e-7_30gev': 'U^{2}=2.86e-7, M_{N}=30 GeV',
    'HNL_4e-12_50gev': 'U^{2}=4e-12, M_{N}=50 GeV',
    'HNL_2.86e-8_80gev': 'U^{2}=2.86e-8, M_{N}=80 GeV',
    'HNL_5e-12_50gev': 'U^{2}=5e-12, M_{N}=50 GeV',
    'HNL_4e-10_80gev': 'U^{2}=4e-10, M_{N}=80 GeV',
    'HNL_4e-8_10gev': 'U^{2}=4e-8, M_{N}=10 GeV',
    'HNL_6.67e-8_60gev': 'U^{2}=6.67e-8, M_{N}=60 GeV',
}

scolors = {
    'HNL_2.86e-12_30gev': ROOT.kBlue-4,
    'HNL_2.86e-7_30gev': ROOT.kOrange+1,
    'HNL_6.67e-8_60gev': ROOT.kRed-4,
    'HNL_2.86e-8_80gev': ROOT.kBlue-1,
    'HNL_4e-8_10gev': ROOT.kAzure+6,
}

for cut in CUTS:

    extralab = LABELS[cut]

    for variable in VARIABLES_ALL:

        canvas = ROOT.TCanvas("", "", 800, 800)

        nsig = len(signals)
        nbkg = len(backgrounds)

        #legend coordinates and style
        legsize = 0.04*nsig
        legsize2 = 0.04*nbkg
        leg = ROOT.TLegend(0.16, 0.80 - legsize, 0.45, 0.74)
        leg.SetFillColor(0)
        leg.SetFillStyle(0)
        leg.SetLineColor(0)
        leg.SetShadowColor(0)
        leg.SetTextSize(0.025)
        leg.SetTextFont(42)

        leg2 = ROOT.TLegend(0.70, 0.80 - legsize2, 0.88, 0.74)
        leg2.SetFillColor(0)
        leg2.SetFillStyle(0)
        leg2.SetLineColor(0)
        leg2.SetShadowColor(0)
        leg2.SetTextSize(0.025)
        leg2.SetTextFont(42)

        #global arrays for histos and colors
        histos = []
        colors = []

        #loop over files for signals and backgrounds and assign corresponding colors and titles
        for s in signals:
            fin = f"{DIRECTORY}{s}_{cut}_histo.root"
            with ROOT.TFile(fin) as tf:
                h = tf.Get(variable)
                hh = copy.deepcopy(h)
                hh.SetDirectory(0)
            histos.append(hh)
            colors.append(scolors[s])
            leg.AddEntry(histos[-1], slegend[s], "l")

        for b in backgrounds:
            fin = f"{DIRECTORY}{b}_{cut}_histo.root"
            with ROOT.TFile(fin) as tf:
                h = tf.Get(variable)
                hh = copy.deepcopy(h)
                hh.SetDirectory(0)
            histos.append(hh)
            colors.append(bcolors[b])
            leg2.AddEntry(histos[-1], blegend[b], "f")

        if nbkg!=0:

            #drawing stack for backgrounds
            hStackBkg = ROOT.THStack("hStackBkg", "")
            hStackBkg.SetMinimum(1e-6)
            hStackBkg.SetMaximum(1e20)
            BgMCHistYieldsDic = {}
            for i in range(nsig, nsig+nbkg):
                h = histos[i]
                h.SetLineWidth(1)
                h.SetLineColor(ROOT.kBlack)
                h.SetFillColor(colors[i])
                if h.Integral() > 0:
                    BgMCHistYieldsDic[h.Integral()] = h
                else:
                    BgMCHistYieldsDic[-1*nbkg] = h

            # sort stack by yields (smallest to largest)
            BgMCHistYieldsDic = sorted_dict_values(BgMCHistYieldsDic)
            for h in BgMCHistYieldsDic:
                hStackBkg.Add(h)

            #draw the histograms
            hStackBkg.Draw("HIST")

            # add the signal histograms
            for i in range(nsig):
                h = histos[i]
                h.SetLineWidth(3)
                h.SetLineColor(colors[i])
                h.Draw("HIST SAME")

            hStackBkg.GetYaxis().SetTitle("Events")
            hStackBkg.GetXaxis().SetTitle("{}".format(variable))
            #hStackBkg.GetYaxis().SetTitleOffset(1.5)
            hStackBkg.GetXaxis().SetTitleOffset(1.2)
            #hStackBkg.GetXaxis().SetLimits(1, 1000)

        else: 
             # add the signal histograms
            for i in range(nsig):
                h = histos[i]
                h.SetLineWidth(3)
                h.SetLineColor(colors[i])
                if i == 0:
                    h.Draw("HIST")
                    h.GetYaxis().SetTitle("Events")
                    h.GetXaxis().SetTitle(histos[i].GetXaxis().GetTitle())
                    #h.GetXaxis().SetTitle("{}".format(variable))
                    h.GetYaxis().SetRangeUser(1e-6,1e15)
                    #h.GetYaxis().SetTitleOffset(1.5)
                    h.GetXaxis().SetTitleOffset(1.2)
                    #h.GetXaxis().SetLimits(1, 1000)
                else: 
                    h.Draw("HIST SAME")

        

        #labels around the plot
        if 'ee' in collider:
            leftText = 'FCCAnalyses: FCC-ee Simulation (Delphes)'
        rightText = f'#sqrt{{s}} = {energy} GeV, L={intLumi} ab^{{-1}}'

        latex = ROOT.TLatex()
        latex.SetNDC()

        text = '#bf{#it{'+rightText+'}}'
        latex.SetTextSize(0.03)
        latex.DrawLatex(0.18, 0.84, text)

        text = '#bf{#it{' + ana_tex + '}}'
        latex.SetTextSize(0.03)
        latex.DrawLatex(0.18, 0.80, text)

        text = '#bf{#it{' + extralab + '}}'
        latex.SetTextSize(0.02)
        latex.DrawLatex(0.18, 0.76, text)

        leg.Draw()
        leg2.Draw()

        latex.SetTextAlign(31)
        text = '#it{' + leftText + '}'
        latex.SetTextSize(0.03)
        latex.DrawLatex(0.92, 0.92, text)

        # Set Logarithmic scales for both x and y axes
        #canvas.SetLogx()
        canvas.SetLogy()
        canvas.SetTicks(1, 1)
        canvas.SetLeftMargin(0.14)
        canvas.SetRightMargin(0.08)
        canvas.GetFrame().SetBorderSize(12)

        canvas.RedrawAxis()
        canvas.Modified()
        canvas.Update()

        dir = DIR_PLOTS + "/" + cut + "/"
        make_dir_if_not_exists(dir)

        canvas.SaveAs(dir + variable + ".png")
        canvas.SaveAs(dir+ variable + ".pdf")