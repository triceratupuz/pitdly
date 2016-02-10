<CsoundSynthesizer> 
<CsOptions> 
</CsOptions> 
<CsInstruments> 
sr = $SRATE
ksmps = $KRATE
nchnls = 2
0dbfs = 1
zakinit 9, 1

;bus channels
;gkbpm chnexport "gkbpm", 3 
gktaptempo_t init 0;last tap temp time
gktaptempo_c init 0;counter of taps
;gkv chnexport "count", 3 

chn_k "test_sound", 1;in Channel

chn_k "gkbpm_from_cs", 2;out Channel
chn_k "gkbpmt_to_cs", 1;In Channel
chn_k "metro_from_cs", 2;out Channel

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



instr 1;globals
print p1
ktest chnget "test_sound"
if ktest == 1 then
	ktrig metro gkbpmP / 60
	String  sprintfk {{i 2 0 %d.%d}}, int(60 / gkbpmP), int(frac(60 / gkbpmP) * 100)
	scoreline String, ktrig
endif
endin


instr 2;test
ipitch unirand 48
ivol unirand 0.2
ipos unirand 1.0
kenve linseg 0, 0.01, 1, 0.01, 0.5, p3 - 0.03, 0.4, 0.01, 0
ao oscil 0.1 + ivol, cpsmidinn(48 + ipitch), 1
alh, arh pan2 ao, ipos

;kinGainDly chnget "inGainDly"
kind = 11
kinGainDly tab kind, 99

zawm alh * kinGainDly, 0
zawm arh * kinGainDly, 1
zawm ao, 2
;outs ao, ao
endin



instr 3;input
ainl, ainr ins

;mono/stereo input operation
kind = 0
kstereoin tab kind, 99

kind = 11
kinGainDly tab kind, 99

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

atest0 zar 0
atest1 zar 1
atest2 zar 2
zacl 0, 2

zawm (aoutl + atest0) * kinGainDlyP, 0
zawm (aoutr + atest1) * kinGainDlyP, 1
zawm (aoutd + atest2) * kinGainDlyP, 2

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
gkbpmP port gkbpm, 0.05
;printk2 kmetrotrig
;printk2 gkbpmP
;printks "gkbpm: %f - kbpm: %f\n", .2 , gkbpm, kbpm

;global fsig for
;pitch shifting
ifftsize  = 1024 * 2
ioverlap  = ifftsize / 4
iwinsize  = ifftsize
iwintype = 1
gfsig  pvsanal   (aoutd + atest2) * kinGainDly, ifftsize, ioverlap, iwinsize, iwintype ; analyse it


endin





instr 4;tap tempo
;print p1
;gktaptempo_t init 0;last tap temp time
;gktaptempo_c init 0;counter of taps
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
print p1
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
print p1
kind = 1
ktime tab kind, 99
kind = 2
kfeed tab kind, 99
;filters
kind = 5
khp tab kind, 99
khpp port khp, 0.05
kind = 6
klp tab kind, 99
klpp port klp, 0.05
;direct input
kind = 3
kdir tab kind, 99
kdirp port kdir, 0.05

ainL zar 5
ainR zar 6

adirectL zar 0
adirectR zar 1

adL delayr 60
atapL deltap ktime * 60 / gkbpmP
ahpL buthp atapL, khpp
alpL butlp ahpL, klpp
	delayw ainR + kfeed * alpL + adirectL * kdirp

adR delayr 60
atapR deltap ktime * 60 / gkbpmP
ahpR buthp atapR, khpp
alpR butlp ahpR, klpp
	delayw ainL + kfeed * alpR + adirectR * kdirp

zawm alpL, 7
zawm alpR, 8
endin



instr 50; output mixer and VUmeter
;print p1
kdecl linseg 0, .1, 1
;volume compensation
kinsnum init 30
kacti30 active kinsnum
kacti30 = (kacti30 < 1 ? 1 : kacti30)
kacti30p port kacti30, .02

;Mixer
;kdirect chnget "outdirectV";outmix direct volume
kind = 7
kdirect tab kind, 99
;kdly chnget "outdlyV";outmix delay volume
kind = 8
kdly tab kind, 99
;krecyc chnget "outrecycV"
kind = 9
krecyc tab kind, 99
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
;klimit chnget "limitON"
kind = 10
klimit tab kind, 99
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

f 99 0 16 -2 0;recycle delay table
;index
;0 - mono stereo input
;1 - recycle time
;2 - recycle feedback
;3 - recycle input from input
;4 - 
;5 - recycle hp
;6 - recycle lp
;7 - Outmixer direct volume
;8 - Outmixer delay volume
;9 - Outmixer recycle volume
;10 - Outmixer limiter
;11 - input gain


;ftables from 100 and on used for delay istances perameters
f 100 0 16 -2 0;dummy table



;Run
i 1 0 3600
i 3 0 3600
i 39 0 3600
i 50 0 3600

</CsScore> 
</CsoundSynthesizer> 
