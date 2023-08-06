#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: This script is used for extract UTR sequences once given coordinate and transcript sequence.
'''



from .FunctionDefinition import *


def extract_UTRs(transcriptFile,startCodonCoorDict,stopCodonCoorDict,output_prefix):
	'''
	This function is used for extracting UTR sequences of a given sequence.
	'''
	trans_sequence_dict=fastaIter(transcriptFile)
	in_selectTrans=set(trans_sequence_dict.keys())
	in_selectTrans=in_selectTrans.intersection(startCodonCoorDict.keys())
	i=0
	UTR5_zero=0
	UTR3_zero=0
	CDS_zero=0
	with open(output_prefix+"_5UTR.fa",'w') as f1,open(output_prefix+"_CDS.fa",'w') as f2,open(output_prefix+"_3UTR.fa",'w') as f3:
		for trans in in_selectTrans:
			trans_sequence=trans_sequence_dict[trans]
			startCoor=int(startCodonCoorDict[trans])-1 # 0-based
			stopCoor=int(stopCodonCoorDict[trans])-3 # 0-based , the first base of stop codon
			UTR5_sequence=trans_sequence[:startCoor]
			cds_sequence=trans_sequence[startCoor:(stopCoor+3)]
			cds_sequence=trans_sequence[startCoor:(stopCoor+3)]
			UTR3_sequence=trans_sequence[(stopCoor+3):]
			UTR5_length=len(UTR5_sequence)
			cds_length=len(cds_sequence)
			UTR3_length=len(UTR3_sequence)
			if cds_length%3 !=0:
				i+=1
			if UTR3_length==0:
				UTR3_zero+=1
				continue
			else:
				f3.write("%s%s\n" %(">",str(trans)+" "+str(UTR3_length)))
				f3.write("%s\n" %(UTR3_sequence))
			if UTR5_length==0:
				UTR5_zero+=0
				continue
			else:
				f1.write("%s%s\n" %(">",str(trans)+" "+str(UTR5_length)))
				f1.write("%s\n" %(UTR5_sequence))
			if cds_length==0:
				CDS_zero+=0
				continue
			else:
				f2.write("%s%s\n" %(">",str(trans)+" "+str(cds_length)))
				f2.write("%s\n" %(cds_sequence))
	print("Notes: There are " + str(i) +" transcripts whose cds sequence cannot be divided by 3!",file=sys.stderr)
	print("Notes: There are " + str(UTR5_zero) +" transcripts with 5UTR length equaling 0 which will be filtered in 5UTR sequence!",file=sys.stderr)
	print("Notes: There are " + str(UTR3_zero) +" transcripts with 3UTR length equaling 0 which will be filtered in 3UTR sequence!",file=sys.stderr)
	print("Notes: There are " + str(CDS_zero) +" transcripts with CDS length equaling 0 which will be filtered in CDS sequence!",file=sys.stderr)

def main():
	parser=create_parser_for_UTR_sequence_extraction()
	(options,args)=parser.parse_args()
	if not options.transcriptFile or not options.coorFile or not options.output_prefix:
		raise IOError("Please reset your parameters!")
	startCodonCoorDict,stopCodonCoorDict=parse_coorFile(options.coorFile)
	print("Start extracting UTR sequences...",file=sys.stderr)
	extract_UTRs(options.transcriptFile,startCodonCoorDict,stopCodonCoorDict,options.output_prefix)
	print("Finish the step of UTR sequences extracting!",file=sys.stderr)

if __name__=="__main__":
	main()