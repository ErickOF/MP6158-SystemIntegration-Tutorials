<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE eagle SYSTEM "eagle.dtd">
<eagle version="9.6.2">
<drawing>
<settings>
<setting alwaysvectorfont="no"/>
<setting verticaltext="up"/>
</settings>
<grid distance="0.1" unitdist="inch" unit="inch" style="lines" multiple="1" display="no" altdistance="0.01" altunitdist="inch" altunit="inch"/>
<layers>
<layer number="1" name="Top" color="4" fill="1" visible="no" active="no"/>
<layer number="16" name="Bottom" color="1" fill="1" visible="no" active="no"/>
<layer number="17" name="Pads" color="2" fill="1" visible="no" active="no"/>
<layer number="18" name="Vias" color="2" fill="1" visible="no" active="no"/>
<layer number="19" name="Unrouted" color="6" fill="1" visible="no" active="no"/>
<layer number="20" name="Dimension" color="24" fill="1" visible="no" active="no"/>
<layer number="21" name="tPlace" color="7" fill="1" visible="no" active="no"/>
<layer number="22" name="bPlace" color="7" fill="1" visible="no" active="no"/>
<layer number="23" name="tOrigins" color="15" fill="1" visible="no" active="no"/>
<layer number="24" name="bOrigins" color="15" fill="1" visible="no" active="no"/>
<layer number="25" name="tNames" color="7" fill="1" visible="no" active="no"/>
<layer number="26" name="bNames" color="7" fill="1" visible="no" active="no"/>
<layer number="27" name="tValues" color="7" fill="1" visible="no" active="no"/>
<layer number="28" name="bValues" color="7" fill="1" visible="no" active="no"/>
<layer number="29" name="tStop" color="7" fill="3" visible="no" active="no"/>
<layer number="30" name="bStop" color="7" fill="6" visible="no" active="no"/>
<layer number="31" name="tCream" color="7" fill="4" visible="no" active="no"/>
<layer number="32" name="bCream" color="7" fill="5" visible="no" active="no"/>
<layer number="33" name="tFinish" color="6" fill="3" visible="no" active="no"/>
<layer number="34" name="bFinish" color="6" fill="6" visible="no" active="no"/>
<layer number="35" name="tGlue" color="7" fill="4" visible="no" active="no"/>
<layer number="36" name="bGlue" color="7" fill="5" visible="no" active="no"/>
<layer number="37" name="tTest" color="7" fill="1" visible="no" active="no"/>
<layer number="38" name="bTest" color="7" fill="1" visible="no" active="no"/>
<layer number="39" name="tKeepout" color="4" fill="11" visible="no" active="no"/>
<layer number="40" name="bKeepout" color="1" fill="11" visible="no" active="no"/>
<layer number="41" name="tRestrict" color="4" fill="10" visible="no" active="no"/>
<layer number="42" name="bRestrict" color="1" fill="10" visible="no" active="no"/>
<layer number="43" name="vRestrict" color="2" fill="10" visible="no" active="no"/>
<layer number="44" name="Drills" color="7" fill="1" visible="no" active="no"/>
<layer number="45" name="Holes" color="7" fill="1" visible="no" active="no"/>
<layer number="46" name="Milling" color="3" fill="1" visible="no" active="no"/>
<layer number="47" name="Measures" color="7" fill="1" visible="no" active="no"/>
<layer number="48" name="Document" color="7" fill="1" visible="no" active="no"/>
<layer number="49" name="Reference" color="7" fill="1" visible="no" active="no"/>
<layer number="51" name="tDocu" color="7" fill="1" visible="no" active="no"/>
<layer number="52" name="bDocu" color="7" fill="1" visible="no" active="no"/>
<layer number="88" name="SimResults" color="9" fill="1" visible="yes" active="yes"/>
<layer number="89" name="SimProbes" color="9" fill="1" visible="yes" active="yes"/>
<layer number="90" name="Modules" color="5" fill="1" visible="yes" active="yes"/>
<layer number="91" name="Nets" color="2" fill="1" visible="yes" active="yes"/>
<layer number="92" name="Busses" color="1" fill="1" visible="yes" active="yes"/>
<layer number="93" name="Pins" color="2" fill="1" visible="no" active="yes"/>
<layer number="94" name="Symbols" color="4" fill="1" visible="yes" active="yes"/>
<layer number="95" name="Names" color="7" fill="1" visible="yes" active="yes"/>
<layer number="96" name="Values" color="7" fill="1" visible="yes" active="yes"/>
<layer number="97" name="Info" color="7" fill="1" visible="yes" active="yes"/>
<layer number="98" name="Guide" color="6" fill="1" visible="yes" active="yes"/>
</layers>
<schematic xreflabel="%F%N/%S.%C%R" xrefpart="/%S.%C%R">
<libraries>
<library name="ad5940">
<description>AD5940
High Precision, Impedance, and Electrochemical Front End
https://wiki.analog.com/resources/eval/user-guides/ad5940</description>
<packages>
<package name="WLCSP56">
<description>WLCSP56 package for AD5940</description>
<smd name="A8" x="0" y="0" dx="0.28" dy="0.28" layer="1" roundness="100" stop="no" cream="no"/>
<wire x1="-0.68" y1="-2.98" x2="3.48" y2="-2.98" width="0.2032" layer="51"/>
<wire x1="3.48" y1="-2.98" x2="3.48" y2="0.58" width="0.2032" layer="51"/>
<wire x1="3.48" y1="0.58" x2="-0.68" y2="0.58" width="0.2032" layer="51"/>
<wire x1="-0.68" y1="0.58" x2="-0.68" y2="-2.98" width="0.2032" layer="51"/>
<text x="-0.8" y="1.2" size="1.27" layer="25">&gt;NAME</text>
<text x="-0.8" y="-4.6" size="1.27" layer="27">&gt;VALUE</text>
<rectangle x1="-0.68" y1="-0.02" x2="-0.08" y2="0.58" layer="51"/>
<smd name="A7" x="0.4" y="0" dx="0.28" dy="0.28" layer="1" roundness="100" rot="R180" stop="no" cream="no"/>
<smd name="A6" x="0.8" y="0" dx="0.28" dy="0.28" layer="1" roundness="100" rot="R180" stop="no" cream="no"/>
<smd name="A5" x="1.2" y="0" dx="0.28" dy="0.28" layer="1" roundness="100" rot="R180" stop="no" cream="no"/>
<smd name="A4" x="1.6" y="0" dx="0.28" dy="0.28" layer="1" roundness="100" rot="R180" stop="no" cream="no"/>
<smd name="A3" x="2" y="0" dx="0.28" dy="0.28" layer="1" roundness="100" rot="R180" stop="no" cream="no"/>
<smd name="A2" x="2.4" y="0" dx="0.28" dy="0.28" layer="1" roundness="100" rot="R180" stop="no" cream="no"/>
<smd name="A1" x="2.8" y="0" dx="0.28" dy="0.28" layer="1" roundness="100" rot="R180" stop="no" cream="no"/>
<smd name="B8" x="0" y="-0.4" dx="0.28" dy="0.28" layer="1" roundness="100" stop="no" cream="no"/>
<smd name="B7" x="0.4" y="-0.4" dx="0.28" dy="0.28" layer="1" roundness="100" rot="R180" stop="no" cream="no"/>
<smd name="B6" x="0.8" y="-0.4" dx="0.28" dy="0.28" layer="1" roundness="100" rot="R180" stop="no" cream="no"/>
<smd name="B5" x="1.2" y="-0.4" dx="0.28" dy="0.28" layer="1" roundness="100" rot="R180" stop="no" cream="no"/>
<smd name="B4" x="1.6" y="-0.4" dx="0.28" dy="0.28" layer="1" roundness="100" rot="R180" stop="no" cream="no"/>
<smd name="B3" x="2" y="-0.4" dx="0.28" dy="0.28" layer="1" roundness="100" rot="R180" stop="no" cream="no"/>
<smd name="B2" x="2.4" y="-0.4" dx="0.28" dy="0.28" layer="1" roundness="100" rot="R180" stop="no" cream="no"/>
<smd name="B1" x="2.8" y="-0.4" dx="0.28" dy="0.28" layer="1" roundness="100" rot="R180" stop="no" cream="no"/>
<smd name="C8" x="0" y="-0.8" dx="0.28" dy="0.28" layer="1" roundness="100" stop="no" cream="no"/>
<smd name="C7" x="0.4" y="-0.8" dx="0.28" dy="0.28" layer="1" roundness="100" rot="R180" stop="no" cream="no"/>
<smd name="C6" x="0.8" y="-0.8" dx="0.28" dy="0.28" layer="1" roundness="100" rot="R180" stop="no" cream="no"/>
<smd name="C5" x="1.2" y="-0.8" dx="0.28" dy="0.28" layer="1" roundness="100" rot="R180" stop="no" cream="no"/>
<smd name="C4" x="1.6" y="-0.8" dx="0.28" dy="0.28" layer="1" roundness="100" rot="R180" stop="no" cream="no"/>
<smd name="C3" x="2" y="-0.8" dx="0.28" dy="0.28" layer="1" roundness="100" rot="R180" stop="no" cream="no"/>
<smd name="C2" x="2.4" y="-0.8" dx="0.28" dy="0.28" layer="1" roundness="100" rot="R180" stop="no" cream="no"/>
<smd name="C1" x="2.8" y="-0.8" dx="0.28" dy="0.28" layer="1" roundness="100" rot="R180" stop="no" cream="no"/>
<smd name="D8" x="0" y="-1.2" dx="0.28" dy="0.28" layer="1" roundness="100" stop="no" cream="no"/>
<smd name="D7" x="0.4" y="-1.2" dx="0.28" dy="0.28" layer="1" roundness="100" rot="R180" stop="no" cream="no"/>
<smd name="D6" x="0.8" y="-1.2" dx="0.28" dy="0.28" layer="1" roundness="100" rot="R180" stop="no" cream="no"/>
<smd name="D5" x="1.2" y="-1.2" dx="0.28" dy="0.28" layer="1" roundness="100" rot="R180" stop="no" cream="no"/>
<smd name="D4" x="1.6" y="-1.2" dx="0.28" dy="0.28" layer="1" roundness="100" rot="R180" stop="no" cream="no"/>
<smd name="D3" x="2" y="-1.2" dx="0.28" dy="0.28" layer="1" roundness="100" rot="R180" stop="no" cream="no"/>
<smd name="D2" x="2.4" y="-1.2" dx="0.28" dy="0.28" layer="1" roundness="100" rot="R180" stop="no" cream="no"/>
<smd name="D1" x="2.8" y="-1.2" dx="0.28" dy="0.28" layer="1" roundness="100" rot="R180" stop="no" cream="no"/>
<smd name="E8" x="0" y="-1.6" dx="0.28" dy="0.28" layer="1" roundness="100" stop="no" cream="no"/>
<smd name="E7" x="0.4" y="-1.6" dx="0.28" dy="0.28" layer="1" roundness="100" rot="R180" stop="no" cream="no"/>
<smd name="E6" x="0.8" y="-1.6" dx="0.28" dy="0.28" layer="1" roundness="100" rot="R180" stop="no" cream="no"/>
<smd name="E5" x="1.2" y="-1.6" dx="0.28" dy="0.28" layer="1" roundness="100" rot="R180" stop="no" cream="no"/>
<smd name="E4" x="1.6" y="-1.6" dx="0.28" dy="0.28" layer="1" roundness="100" rot="R180" stop="no" cream="no"/>
<smd name="E3" x="2" y="-1.6" dx="0.28" dy="0.28" layer="1" roundness="100" rot="R180" stop="no" cream="no"/>
<smd name="E2" x="2.4" y="-1.6" dx="0.28" dy="0.28" layer="1" roundness="100" rot="R180" stop="no" cream="no"/>
<smd name="E1" x="2.8" y="-1.6" dx="0.28" dy="0.28" layer="1" roundness="100" rot="R180" stop="no" cream="no"/>
<smd name="F8" x="0" y="-2" dx="0.28" dy="0.28" layer="1" roundness="100" stop="no" cream="no"/>
<smd name="F7" x="0.4" y="-2" dx="0.28" dy="0.28" layer="1" roundness="100" rot="R180" stop="no" cream="no"/>
<smd name="F6" x="0.8" y="-2" dx="0.28" dy="0.28" layer="1" roundness="100" rot="R180" stop="no" cream="no"/>
<smd name="F5" x="1.2" y="-2" dx="0.28" dy="0.28" layer="1" roundness="100" rot="R180" stop="no" cream="no"/>
<smd name="F4" x="1.6" y="-2" dx="0.28" dy="0.28" layer="1" roundness="100" rot="R180" stop="no" cream="no"/>
<smd name="F3" x="2" y="-2" dx="0.28" dy="0.28" layer="1" roundness="100" rot="R180" stop="no" cream="no"/>
<smd name="F2" x="2.4" y="-2" dx="0.28" dy="0.28" layer="1" roundness="100" rot="R180" stop="no" cream="no"/>
<smd name="F1" x="2.8" y="-2" dx="0.28" dy="0.28" layer="1" roundness="100" rot="R180" stop="no" cream="no"/>
<smd name="G8" x="0" y="-2.4" dx="0.28" dy="0.28" layer="1" roundness="100" stop="no" cream="no"/>
<smd name="G7" x="0.4" y="-2.4" dx="0.28" dy="0.28" layer="1" roundness="100" rot="R180" stop="no" cream="no"/>
<smd name="G6" x="0.8" y="-2.4" dx="0.28" dy="0.28" layer="1" roundness="100" rot="R180" stop="no" cream="no"/>
<smd name="G5" x="1.2" y="-2.4" dx="0.28" dy="0.28" layer="1" roundness="100" rot="R180" stop="no" cream="no"/>
<smd name="G4" x="1.6" y="-2.4" dx="0.28" dy="0.28" layer="1" roundness="100" rot="R180" stop="no" cream="no"/>
<smd name="G3" x="2" y="-2.4" dx="0.28" dy="0.28" layer="1" roundness="100" rot="R180" stop="no" cream="no"/>
<smd name="G2" x="2.4" y="-2.4" dx="0.28" dy="0.28" layer="1" roundness="100" rot="R180" stop="no" cream="no"/>
<smd name="G1" x="2.8" y="-2.4" dx="0.28" dy="0.28" layer="1" roundness="100" rot="R180" stop="no" cream="no"/>
</package>
</packages>
<symbols>
<symbol name="AD5940">
<description>Symbol for AD5940</description>
<wire x1="-38.1" y1="-38.1" x2="35.56" y2="-38.1" width="0.2032" layer="94"/>
<wire x1="35.56" y1="-38.1" x2="35.56" y2="35.56" width="0.2032" layer="94"/>
<wire x1="35.56" y1="35.56" x2="-38.1" y2="35.56" width="0.2032" layer="94"/>
<wire x1="-38.1" y1="35.56" x2="-38.1" y2="-38.1" width="0.2032" layer="94"/>
<text x="-5.08" y="1.27" size="1.778" layer="95">&gt;NAME</text>
<text x="-5.08" y="-2.54" size="1.778" layer="96">&gt;VALUE</text>
<pin name="RCAL0" x="-43.18" y="30.48" length="middle"/>
<pin name="RCAL1" x="-43.18" y="27.94" length="middle"/>
<pin name="VBIAS0" x="-43.18" y="22.86" length="middle"/>
<pin name="CE0" x="-43.18" y="17.78" length="middle"/>
<pin name="RE0" x="-43.18" y="15.24" length="middle"/>
<pin name="VZERO0" x="-43.18" y="12.7" length="middle"/>
<pin name="SE0" x="-43.18" y="10.16" length="middle" direction="in"/>
<pin name="DE0" x="-43.18" y="7.62" length="middle"/>
<pin name="DVDD_REG_1V8" x="-7.62" y="-43.18" length="middle" direction="pwr" rot="R90"/>
<pin name="DGND" x="-5.08" y="-43.18" length="middle" direction="pwr" rot="R90"/>
<pin name="DVDD" x="-2.54" y="-43.18" length="middle" direction="pwr" rot="R90"/>
<pin name="!RESET" x="0" y="-43.18" length="middle" rot="R90"/>
<pin name="IOVDD" x="2.54" y="-43.18" length="middle" direction="pwr" rot="R90"/>
<pin name="NC3" x="40.64" y="-22.86" length="middle" direction="nc" rot="R180"/>
<pin name="NC2" x="40.64" y="-20.32" length="middle" direction="nc" rot="R180"/>
<pin name="NC1" x="40.64" y="-17.78" length="middle" direction="nc" rot="R180"/>
<pin name="GPIO7" x="40.64" y="-10.16" length="middle" rot="R180"/>
<pin name="GPIO6" x="40.64" y="-7.62" length="middle" rot="R180"/>
<pin name="GPIO5" x="40.64" y="-5.08" length="middle" rot="R180"/>
<pin name="GPIO4" x="40.64" y="-2.54" length="middle" rot="R180"/>
<pin name="GPIO3" x="40.64" y="0" length="middle" rot="R180"/>
<pin name="GPIO2" x="40.64" y="2.54" length="middle" rot="R180"/>
<pin name="GPIO1" x="40.64" y="5.08" length="middle" rot="R180"/>
<pin name="GPIO0" x="40.64" y="7.62" length="middle" rot="R180"/>
<pin name="!CS" x="40.64" y="15.24" length="middle" rot="R180"/>
<pin name="SCLK" x="40.64" y="17.78" length="middle" rot="R180"/>
<pin name="XTALO" x="7.62" y="40.64" length="middle" rot="R270"/>
<pin name="XTALI" x="5.08" y="40.64" length="middle" rot="R270"/>
<pin name="AGND_REF" x="2.54" y="40.64" length="middle" direction="pwr" rot="R270"/>
<pin name="AVDD" x="0" y="40.64" length="middle" direction="pwr" rot="R270"/>
<pin name="AVDD_REG" x="-2.54" y="40.64" length="middle" direction="pwr" rot="R270"/>
<pin name="VBIAS_CAP" x="-5.08" y="40.64" length="middle" direction="pwr" rot="R270"/>
<pin name="VREF_1V82" x="-7.62" y="40.64" length="middle" direction="pwr" rot="R270"/>
<pin name="VREF_2V5" x="-10.16" y="40.64" length="middle" direction="pwr" rot="R270"/>
<pin name="AGND" x="-12.7" y="40.64" length="middle" direction="pwr" rot="R270"/>
<pin name="RC0_0" x="-43.18" y="2.54" length="middle"/>
<pin name="RC0_1" x="-43.18" y="0" length="middle"/>
<pin name="RC0_2" x="-43.18" y="-2.54" length="middle"/>
<pin name="AIN0" x="-43.18" y="-7.62" length="middle"/>
<pin name="AIN1" x="-43.18" y="-10.16" length="middle"/>
<pin name="AIN2" x="-43.18" y="-12.7" length="middle"/>
<pin name="AIN3" x="-43.18" y="-15.24" length="middle"/>
<pin name="AIN4/LPF0" x="-43.18" y="-17.78" length="middle"/>
<pin name="AIN6" x="-43.18" y="-20.32" length="middle"/>
<pin name="AFE1" x="-43.18" y="-25.4" length="middle"/>
<pin name="AFE2" x="-43.18" y="-27.94" length="middle"/>
<pin name="AFE3" x="-43.18" y="-30.48" length="middle"/>
<pin name="AFE4" x="-43.18" y="-33.02" length="middle"/>
<pin name="MOSI" x="40.64" y="20.32" length="middle" rot="R180"/>
<pin name="MISO" x="40.64" y="22.86" length="middle" rot="R180"/>
<pin name="AGND2" x="15.24" y="40.64" length="middle" direction="pwr" rot="R270"/>
<pin name="DGND2" x="17.78" y="40.64" length="middle" direction="pwr" rot="R270"/>
<pin name="DGND3" x="20.32" y="40.64" length="middle" direction="pwr" rot="R270"/>
<pin name="AVDD2" x="22.86" y="40.64" length="middle" direction="pwr" rot="R270"/>
<pin name="NC5" x="27.94" y="40.64" length="middle" rot="R270"/>
<pin name="NC4" x="25.4" y="40.64" length="middle" rot="R270"/>
</symbol>
</symbols>
<devicesets>
<deviceset name="AD5940">
<description>AD5940
High Precision, Impedance, and Electrochemical Front End
https://wiki.analog.com/resources/eval/user-guides/ad5940</description>
<gates>
<gate name="G$1" symbol="AD5940" x="0" y="0"/>
</gates>
<devices>
<device name="" package="WLCSP56">
<connects>
<connect gate="G$1" pin="!CS" pad="F7"/>
<connect gate="G$1" pin="!RESET" pad="F1"/>
<connect gate="G$1" pin="AFE1" pad="B2"/>
<connect gate="G$1" pin="AFE2" pad="C2"/>
<connect gate="G$1" pin="AFE3" pad="A2"/>
<connect gate="G$1" pin="AFE4" pad="A1"/>
<connect gate="G$1" pin="AGND" pad="C4"/>
<connect gate="G$1" pin="AGND2" pad="E3"/>
<connect gate="G$1" pin="AGND_REF" pad="D5"/>
<connect gate="G$1" pin="AIN0" pad="D2"/>
<connect gate="G$1" pin="AIN1" pad="B3"/>
<connect gate="G$1" pin="AIN2" pad="A3"/>
<connect gate="G$1" pin="AIN3" pad="B5"/>
<connect gate="G$1" pin="AIN4/LPF0" pad="B4"/>
<connect gate="G$1" pin="AIN6" pad="C5"/>
<connect gate="G$1" pin="AVDD" pad="A4"/>
<connect gate="G$1" pin="AVDD2" pad="F2"/>
<connect gate="G$1" pin="AVDD_REG" pad="D8"/>
<connect gate="G$1" pin="CE0" pad="A7"/>
<connect gate="G$1" pin="DE0" pad="B6"/>
<connect gate="G$1" pin="DGND" pad="E4"/>
<connect gate="G$1" pin="DGND2" pad="E5"/>
<connect gate="G$1" pin="DGND3" pad="E6"/>
<connect gate="G$1" pin="DVDD" pad="F3"/>
<connect gate="G$1" pin="DVDD_REG_1V8" pad="G3"/>
<connect gate="G$1" pin="GPIO0" pad="F5"/>
<connect gate="G$1" pin="GPIO1" pad="D6"/>
<connect gate="G$1" pin="GPIO2" pad="E1"/>
<connect gate="G$1" pin="GPIO3" pad="E2"/>
<connect gate="G$1" pin="GPIO4" pad="G7"/>
<connect gate="G$1" pin="GPIO5" pad="F6"/>
<connect gate="G$1" pin="GPIO6" pad="F4"/>
<connect gate="G$1" pin="GPIO7" pad="G4"/>
<connect gate="G$1" pin="IOVDD" pad="G2"/>
<connect gate="G$1" pin="MISO" pad="E8"/>
<connect gate="G$1" pin="MOSI" pad="E7"/>
<connect gate="G$1" pin="NC1" pad="C3"/>
<connect gate="G$1" pin="NC2" pad="D3"/>
<connect gate="G$1" pin="NC3" pad="D4"/>
<connect gate="G$1" pin="NC4" pad="G1"/>
<connect gate="G$1" pin="NC5" pad="G8"/>
<connect gate="G$1" pin="RC0_0" pad="C8"/>
<connect gate="G$1" pin="RC0_1" pad="B8"/>
<connect gate="G$1" pin="RC0_2" pad="C6"/>
<connect gate="G$1" pin="RCAL0" pad="C1"/>
<connect gate="G$1" pin="RCAL1" pad="B1"/>
<connect gate="G$1" pin="RE0" pad="A8"/>
<connect gate="G$1" pin="SCLK" pad="F8"/>
<connect gate="G$1" pin="SE0" pad="A6"/>
<connect gate="G$1" pin="VBIAS0" pad="C7"/>
<connect gate="G$1" pin="VBIAS_CAP" pad="D1"/>
<connect gate="G$1" pin="VREF_1V82" pad="A5"/>
<connect gate="G$1" pin="VREF_2V5" pad="D7"/>
<connect gate="G$1" pin="VZERO0" pad="B7"/>
<connect gate="G$1" pin="XTALI" pad="G5"/>
<connect gate="G$1" pin="XTALO" pad="G6"/>
</connects>
<technologies>
<technology name=""/>
</technologies>
</device>
</devices>
</deviceset>
</devicesets>
</library>
</libraries>
<attributes>
</attributes>
<variantdefs>
</variantdefs>
<classes>
<class number="0" name="default" width="0" drill="0">
</class>
</classes>
<parts>
<part name="U$1" library="ad5940" deviceset="AD5940" device=""/>
</parts>
<sheets>
<sheet>
<plain>
</plain>
<instances>
<instance part="U$1" gate="G$1" x="0" y="0" smashed="yes">
<attribute name="NAME" x="-5.08" y="1.27" size="1.778" layer="95"/>
<attribute name="VALUE" x="-5.08" y="-2.54" size="1.778" layer="96"/>
</instance>
</instances>
<busses>
</busses>
<nets>
</nets>
</sheet>
</sheets>
</schematic>
</drawing>
</eagle>
