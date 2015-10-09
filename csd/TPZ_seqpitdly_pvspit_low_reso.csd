<CsoundSynthesizer> 
<CsOptions> 
;-i adc 
;-o dac
; -d 
</CsOptions> 
<CsInstruments> 
sr = 44100
ksmps = 64
nchnls = 2
0dbfs = 1
zakinit 9, 1

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
gkbpmP init 60



opcode AtanLimit, a, a
ain xin
aout = 2 * taninv(ain) / 3.1415927
xout aout
endop







instr 1;test & input
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

;global fsig for
;pitch shifting
ifftsize  = 1024 * 2
ioverlap  = ifftsize / 4
iwinsize  = ifftsize
iwintype = 1
gfsig  pvsanal   aoutd * kinGainDly, ifftsize, ioverlap, iwinsize, iwintype ; analyse it


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
ainrL zar 7
ainrR zar 8
ainr = ainrL + ainrR
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
kq tab kind, itable
kind = 9
kdist tab kind, itable
kind = 10
kvolin tab kind, itable
kind = 11
kvolinr tab kind, itable
kind = 12
kvol tab kind, itable
kind = 13
kvolr tab kind, itable
kind = 14
kmode tab kind, itable


ftps  pvscale   gfsig, semitone(ksemit), 0, 1, 160         ; transpose it keeping formants
ashift  pvsynth   ftps                     ; synthesise it


ashiftb balance ashift, ain * kdeckl
;delay
adump delayr 60
ares deltap3 ktime * 60 / gkbpmP

krms rms ashiftb
	;envelope follower
	if kmode == 0 then
		ahp buthp ares, klf
		alp lpf18 ahp, khf, kq, kdist
	elseif kmode == 1 then
		ahp buthp ares, klf
		kef = klf + krms * (khf - klf)
		alp lpf18 ahp, kef, kq, kdist
	else
		ahp buthp ares, klf
		kef = klf + (1 - krms) * (khf - klf)
		alp lpf18 ahp, kef, kq, kdist
	endif
	
	delayw ashiftb + kfeed * alp + ainr * kvolinr
apl, apr pan2 alp, kpan
zawm apl * kvol * kdeckl, 3
zawm apr * kvol * kdeckl, 4
zawm apl * kvolr * kdeckl, 5
zawm apr * kvolr * kdeckl, 6

endin


instr 39
zacl 7, 8
endin


instr 40;recycle delay
kind = 1
ktime tab kind, 99
kind = 2
kfeed tab kind, 99

ainL zar 5
ainR zar 6

adL delayr 60
atapL deltap ktime * 60 / gkbpmP
	delayw ainR + kfeed * atapL

adR delayr 60
atapR deltap ktime * 60 / gkbpmP
	delayw ainL + kfeed * atapR

zawm atapL, 7
zawm atapR, 8
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
krecyc chnget "outrecycV"
kdirectP port kdirect, 0.05
kdlyP port kdly, 0.05
krecycP port krecyc, 0.05

adirectl zar 0
adirectr zar 1
adlyl zar 3
adlyr zar 4
arecycl zar 7
arecycr zar 8
atl = kdecl * ((adirectl * kdirectP + kdlyP * adlyl / sqrt(kacti30p)) + (arecycl * krecycP))
atr = kdecl * ((adirectr * kdirectP + kdlyP * adlyr / sqrt(kacti30p)) + (arecycr * krecycP))

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
zacl 0, 6
endin




</CsInstruments> 
<CsScore> 
f1 0 16384 10 1 

f 20 0 0 1 "202244__luckylittleraven__bass01.wav" 0 0 0

f 99 0 4 -2 0;recycle delay table
;ftables from 100 and on used for delay istances perameters
f 100 0 16 -2 0;dummy table



;Run
i1 0 3600
i39 0 3600
i50 0 3600

</CsScore> 
</CsoundSynthesizer> 
