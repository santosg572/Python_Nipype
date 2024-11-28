#Import modules

import nipype
import nipype.interfaces.afni as afni
import nipype.interfaces.freesurfer as fs
import nipype.interfaces.ants as ants
import nipype.interfaces.fsl as fsl
import nipype.interfaces.nipy as nipy
import nipype.interfaces.spm as spm


#Specify experiment specifc parameters

experiment_dir = '~/experiment_folder'
nameofsubjects = ['subject1','subject2','subject3']

#Where can the raw data be found?

grabber = nipype.DataGrabber()
grabber.inputs.base_directory = experiment_dir + '/data'
grabber.inputs.subject_id = nameofsubjects

#Where should the output data be stored at?
sink = nipype.DataSink()
2 Chapter 1. Introduction to Nipype
Nipype Beginner’s Guide, Release 1.0
22 sink.inputs.base_directory = experiment_dir + '/output_folder'
23
24
25 #Create a node for each step of the analysis
26
27 #Motion Correction (AFNI)
28 realign = afni.Retroicor()
29
30 #Coregistration (FreeSurfer)
31 coreg = fs.BBRegister()
32
33 #Normalization (ANTS)
34 normalize = ants.WarpTimeSeriesImageMultiTransform()
35
36 #Smoothing (FSL)
37 smooth = fsl.SUSAN()
38 smooth.inputs.fwhm = 6.0
39
40 #Model Specification (Nipype)
41 modelspec = nipype.SpecifyModel()
42 modelspec.inputs.input_units = 'secs'
43 modelspec.inputs.time_repetition = 2.5
44 modelspec.inputs.high_pass_filter_cutoff = 128.
45
46 #Model Estimation (SPM)
47 modelest = spm.EstimateModel()
48
49 #Contrast Estimation (SPM)
50 contrastest = spm.EstimateContrast()
51 cont1 = ['human_faces', [1 0 0]]
52 cont2 = ['animal_faces', [0 1 0]]
53 contrastest.inputs.contrasts = [cont1, cont2]
54
55 #Statistical Inference (SPM)
56 threshold = spm.Threshold()
57 threshold.inputs.use_fwe_correction = True
58 threshold.inputs.extent_fdr_p_threshold = 0.05
59
60
61 #Create a workflow to connect all those nodes
62 analysisflow = nipype.Workflow()
63
64 #Connect the nodes to each other
65 analysisflow.connect([(grabber -> realign ),
66 (realign -> coreg ),
67 (coreg -> normalize ),
68 (normalize -> smooth ),
69 (smooth -> modelspec ),
70 (modelspec -> modelest ),
71 (modelest -> contrastest),
72 (contrastest -> threshold ),
73 (threshold -> sink )
74 ])
75
76 #Run the workflow in parallel
77 analysisflow.run(mode='parallel')


