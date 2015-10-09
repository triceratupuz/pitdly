<CsoundSynthesizer> 
<CsOptions> 
;-i adc 
;-o dac
; -d 
</CsOptions> 
<CsInstruments> 
sr = 44100
ksmps = 32
nchnls = 2
0dbfs = 1
zakinit 6, 1

; bus channel 
;gkbpm chnexport "gkbpm", 3 
gktaptempo_t init 0;last tap temp time
gktaptempo_c init 0;counter of taps
;gkv chnexport "count", 3 

chn_k "gkbpm_from_cs", 2;out Channel
chn_k "gkbpmt_to_cs", 1;In Channel
chn_k "metro_from_cs", 2;out Channel




chn_k "monostereo", 1;delay input mono or stereo
chn_k "inGainDly", 1;delay input volume
chn_k "outdirectV", 1;outmix direct volume
chn_k "outdlyV", 1;outmix delay volume
chn_k "limitON", 1;limiter activation

chn_k "directvul", 2;direct vumeter LH
chn_k "directvur", 2;direct vumeter RH
chn_k "totalvul", 2;output vumeter LH
chn_k "totalvur", 2;output vumeter RH


gkbpm init 60



opcode AtanLimit, a, a
ain xin
aout = 2 * taninv(ain) / 3.1415927
xout aout
endop



;Delay based pitch shifter
;Semitones control as kontrol signal
opcode PitchShifter_akk, a, akki
;setksmps 10
ain, ksemitones, kquality, ihalfsine xin
;ksemitones number of semitones of trasposition
;kquality quality of the output - adds delay - from 0 to infinity
	imaxdlt init 2
	kdlt = .01 + .1 * kquality
	;ihalfsine	ftgen	0, 0, 2049, 9, 0.5, 1, 0	;HALF SINE  WINDOW FUNCTION USED FOR AMPLITUDE ENVELOPING

	koctfract	=	ksemitones/12			;TRANSPOSITION AS FRACTION OF AN OCTAVE
	kratio		=	octave(koctfract)		;RATIO TO PRODUCE PITCH SHIFT
	krate		=	(kratio-1)/kdlt 			;SUBTRACT 1/1 SPEED

	aphase1		phasor	-krate				;MOVING PHASE 1-0
	aphase2		phasor	-krate, .5			;MOVING PHASE 1-0 - PHASE OFFSET BY 180 DEGREES (.5 RADIANS)

	;What if ihalfine table dimension is increased?
	agate1		tablei	aphase1, ihalfsine, 1, 0, 1	;WINDOW FUNC =HALF SINE
	agate2		tablei	aphase2, ihalfsine, 1, 0, 1	;WINDOW FUNC =HALF SINE

	adlt		interp	kdlt				;CREATE A RATE (INTERPOLATED FROM K-RATE) VERSION OF kdlt
	aout		init	0				;INITIALISE OUTPUT AUDIO SIGNAL (NEEDED FOR FEEDBACK SIGNAL (METHOD 2))

	abuffer		delayr	imaxdlt				;DECLARE DELAY BUFFER
	adelsig1	deltap3	aphase1 * adlt			;VARIABLE TAP
	aGatedSig1	=	adelsig1 * agate1
			delayw	ain

	abuffer		delayr	imaxdlt				;DECLARE DELAY BUFFER
	adelsig2	deltap3	aphase2 * adlt			;VARIABLE TAP
	aGatedSig2	=	adelsig2 * agate2
			delayw	ain

	aout	dcblock2	(aGatedSig1 + aGatedSig2) * 0.5

	xout aout
endop



instr 1;test & input
print p1
;ainl, ainr ins

ainl, ainr diskin2 "202244__luckylittleraven__bass01.wav", 1, 0, 1
;outs ainl, ainl

;ainl oscil .3, 440
;ainr = ainl
;outs ainl, ainl


;mono/stereo input operation
;kstereoin init 0
kstereoin chnget "monostereo"
kinGainDly chnget "inGainDly"
kinGainDlyP port kinGainDly, 0.05
kinGainDlyP init 1
if kstereoin == 0 then
	;only left chennel
	aoutl = ainl
	aoutr = ainl
	aoutd = ainl
else
	;both are summed in the delay
	aoutl = ainl
	aoutr = ainr
	aoutd = (ainl + ainr) * .5
endif

zawm aoutl * kinGainDly, 0
zawm aoutr * kinGainDly, 1
zawm aoutd * kinGainDly , 2


;metronome management
kbpmt changed gkbpm
;printk2 gkbpm
;printk2 gktaptempo_c
kbpm chnget "gkbpm_to_cs"
kbpmt changed kbpm
if kbpmt == 1 then
	gkbpm = kbpm
	chnset gkbpm, "gkbpm_from_cs"
endif

kmetrotrig  metro gkbpm / 60
chnset kmetrotrig, "metro_from_cs"
gkbpmP port gkbpm, 0.01
;printk2 kmetrotrig
;printk2 gkbpm
;printks "gkbpm: %f - kbpm: %f\n", .2 , gkbpm, kbpm
endin





instr 3;tap tempo
;gktaptempo_t init 0;last tap temp time
;gktaptempo_c init 0;counter of taps
;kTimer	timeinsts
kTimer times
;reset after X seconds
if (kTimer - gktaptempo_t) > 3 then
	gktaptempo_c = 0
endif
;Trigger the calculator if not the first tap
if gktaptempo_c > 0 then
	gkbpm = 60 / (kTimer - gktaptempo_t)
	chnset gkbpm, "gkbpm_from_cs"
	chnset gkbpm, "gkbpm_to_cs"
endif
gktaptempo_t = kTimer
gktaptempo_c = gktaptempo_c + 1
turnoff
endin








instr 30; a delay
;print p1
kdeckl linsegr 0, .07, 1, .07, 0
itable = 100 + round(frac(p1) * 1000)
;print itable
;print p4
;i1 tab_i 0, itable
;print i1
ain zar 2
;outs ain, ain
;get parameters
kind = 1
ktime tab kind, itable
kind = 2
ksemit tab kind, itable
kind = 3
kquality tab kind, itable
kind = 4
kfeed tab kind, itable
kind = 5
klf tab kind, itable
kind = 6
khf tab kind, itable
kind = 7
kpan tab kind, itable
kind = 8
kvol tab kind, itable



/*
it tab_i 1, itable
is tab_i 2, itable
;print p1
print it
print is

;pitch shifting
ifftsize  = 2048 * 2
ioverlap  = ifftsize / 4
iwinsize  = ifftsize
iwintype = 1
fsig  pvsanal   ain * kdeckl, ifftsize, ioverlap, iwinsize, iwintype ; analyse it
ftps  pvscale   fsig, semitone(ksemit), 0, 1, 160         ; transpose it keeping formants
ashift  pvsynth   ftps                     ; synthesise it
*/

ashift PitchShifter_akk ain * kdeckl, ksemit, kquality, 10


ashiftb balance ashift, ain * kdeckl
;delay
adump delayr 60
ares deltap3 ktime * 60 / gkbpmP
ahp buthp ares, klf
alp butlp ahp, khf
	delayw ashiftb + kfeed * alp
apl, apr pan2 alp, kpan
zawm apl * kvol * kdeckl, 3
zawm apr * kvol * kdeckl, 4
;zawm ashift, 3
;zawm ain, 4

endin





instr 50; output mixer and VUmeter
kdecl linseg 0, .1, 1
;volume compensation
kinsnum init 30
kacti30 active kinsnum
kacti30 = (kacti30 < 1 ? 1 : kacti30)
kacti30p port kacti30, .02

;Mixer
kdirect chnget "outdirectV";outmix direct volume
kdly chnget "outdlyV";outmix delay volume
kdirectP port kdirect, 0.05
kdlyP port kdly, 0.05

adirectl zar 0
adirectr zar 1
adlyl zar 3
adlyr zar 4
atl = kdecl * (adirectl * kdirectP + kdlyP * adlyl / sqrt(kacti30p))
atr = kdecl * (adirectr * kdirectP + kdlyP * adlyr / sqrt(kacti30p))

;limiter
klimit chnget "limitON"
if klimit == 1 then
	atl AtanLimit atl
	atr AtanLimit atr
endif

;VU meters
ktrigamp metro 5;must be synched with gui
;direct signal
kdirectl_rms max_k adirectl, ktrigamp, 1
kdirectr_rms max_k adirectr, ktrigamp, 1
kdirectl_rms_db = dbfsamp(kdirectl_rms)
kdirectr_rms_db = dbfsamp(kdirectr_rms)
;total signal
ktl_rms max_k atl, ktrigamp, 1
ktr_rms max_k atr, ktrigamp, 1
ktl_rms_db = dbfsamp(ktl_rms)
ktr_rms_db = dbfsamp(ktr_rms)

;transmits VUmeters to GUI
if ktrigamp == 1 then
	chnset kdirectl_rms_db, "directvul"
	chnset kdirectr_rms_db, "directvur"
	chnset ktl_rms_db, "totalvul"
	chnset ktr_rms_db, "totalvur"
endif



outs atl, atr
zacl 0, 5
endin




</CsInstruments> 
<CsScore> 
f1 0 16384 10 1 
;f10	0	2049	9	0.5	1	0;HALF SINE  WINDOW FUNCTION USED FOR AMPLITUDE ENVELOPING
f10	0	16385	9	0.5	1	0;HALF SINE  WINDOW FUNCTION USED FOR AMPLITUDE ENVELOPING

f 20 0 0 1 "202244__luckylittleraven__bass01.wav" 0 0 0

;ftables from 100 and on used for delay istances perameters




; run for 30 secs 
i1 0 3600
i50 0 3600

</CsScore> 
</CsoundSynthesizer> 
