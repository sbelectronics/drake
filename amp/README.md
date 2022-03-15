# Drake R-4C Amplifier Mod

Based on Bob Sherwood's [April 1979 Ham Radio Article](https://worldradiohistory.com/Archive-DX/Ham%20Radio/70s/Ham-Radio-197904.pdf)

Connecting it (my summary below; Just read Sherwood's article for the real source)

* Disconnect the existing amplifier transistor Q11 collector at its solder lug.
* Disconnect the 100 ohm driver resistor (R84) on the nearby audio pcboard
* Disconnect the existing wire to the wiper to the AF audio pot
* Connect the V+ to the terminal with the large blue wire at the audio pcboard. You can verify this to be approximately 16 VDC.
* Connect the "IN" footprint's signal and ground to the wiper and ground on the AF audio pot. This should be the only ground you connect to this board. Do not connect the other grounds.
* Connect the "OUT" signal to the headphone jack. Install an 0.01uF bypass cap between headphone jack's terminals.

Revision 0.1

* The first board I used in my R-4C
* The 390 ohm resistor gets a little bit hot. Suggest sizing up to 1/2 watt. 1/4 watt is fine elsewhere.
* Some footprints are a little tight.
* The mounting hole is wired to the board ground. This violates Sherwood's instructions (didn't make any difference in my installation) and will be removed in the next revision.
* There is no pad underneath the regulator. Solder a jumper wire between the regulator and the nearby ground pad to ground the tab on the regulator. This will be corrected in the next revision
* As per Sherwood's recommendation, use a monolithic ceramic for the 1uF cap closest to the regulator. 



For more ham radio projects and electronics projects see www.smbaker.com. 