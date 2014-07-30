## -##- coding: utf-8 -##-
## Adapted from
##
## International Phonetic Alphabet Chart in Unicode and XHTML/CSS
## Copyright (C) 2004-2009 Weston Ruter <https://github.com/westonruter/ipa-chart/>
##
## This program is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License
## as published by the Free Software Foundation; either version 2
## of the License, or (at your option) any later version.
##
## This program is distributed in the hope that it will core useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
##/
<!% from __future__ import unicode_literals %>
<%def name="chart(segments, segment_handler)">
    <div class="ipa" id="pulmonicConsonants">
		<h2>Consonants (Pulmonic)</h2>
		<table>
			<!--<caption>Where symbols appear in pairs, the one to the right
			represents a voiced consonant. Shaded areas denote articulations
			judged impossible.</caption>-->
			<colgroup width="0*" />
			<colgroup />
			<colgroup />
			<colgroup />
			<colgroup />
			<colgroup />
			<colgroup />
			<colgroup />
			<colgroup />
			<colgroup />
			<colgroup />
			<colgroup />
			<thead>
			<tr>
				<td></td>
				<th class="place">Bilabial</th>
				<th class="place">Labiodental</th>
				<th class="place">Dental</th>
				<th class="place">Alveolar</th>
				<th class="place">Postalveolar</th>
				<th class="place">Retroflex</th>
				<th class="place">Palatal</th>
				<th class="place">&nbsp;Velar&nbsp;</th> <!-- Note: spaces to prevent MSIE from wrapping some symbols -->
				<th class="place">Uvular</th>
				<th class="place">Pharyngeal</th>
				<th class="place">Glottal</th>
			</tr>
			</thead>
			<tbody>
			<tr>
				<th class="manner">Plosive</th>
				<td>
					<span title="U+0070: LATIN SMALL LETTER P" class='voiceless'>${segment_handler(request, u'p', segments)}</span>
					<span title="U+0062: LATIN SMALL LETTER B" class='voiced'>${segment_handler(request, u'b', segments)}</span>
				</td>
				<td></td>
				<td>
                    <span title="U+0074-U+032A: LATIN SMALL LETTER T - COMBINING BRIDGE BELOW " class='voiceless'>${segment_handler(request, u't\u032a', segments)}</span>
                    <span title="U+0064-U+032A: LATIN SMALL LETTER D - COMBINING BRIDGE BELOW " class='voiced'>${segment_handler(request, u'd\u032a', segments)}</span>
                </td>
				<td>
					<span title="U+0074: LATIN SMALL LETTER T" class='voiceless'>${segment_handler(request, u't', segments)}</span>
					<span title="U+0064: LATIN SMALL LETTER D" class='voiced'>${segment_handler(request, u'd', segments)}</span>
				</td>
				<td></td>
				<td>
					<span title="U+0288: LATIN SMALL LETTER T WITH RETROFLEX HOOK" class='voiceless'>${segment_handler(request, u'ʈ', segments)}</span>
					<span title="U+0256: LATIN SMALL LETTER D WITH TAIL" class='voiced'>${segment_handler(request, u'ɖ', segments)}</span>
				</td>
				<td>
					<span title="U+0063: LATIN SMALL LETTER C" class='voiceless'>${segment_handler(request, u'c', segments)}</span>
					<span title="U+025F: LATIN SMALL LETTER DOTLESS J WITH STROKE" class='voiced'>${segment_handler(request, u'ɟ', segments)}</span>
				</td>
				<td>
					<span title="U+006B: LATIN SMALL LETTER K" class='voiceless'>${segment_handler(request, u'k', segments)}</span>
					<span title="U+0261: LATIN SMALL LETTER SCRIPT G" class='voiced'>${segment_handler(request, u'ɡ', segments)}</span>
				</td>
				<td>
					<span title="U+0071: LATIN SMALL LETTER Q" class='voiceless'>${segment_handler(request, u'q', segments)}</span>
					<span title="U+0262: LATIN LETTER SMALL CAPITAL G" class='voiced'>${segment_handler(request, u'ɢ', segments)}</span>
				</td>
				<td>
					<span class='voiceless'></span>
					<span class='voiced impossible'>&nbsp;</span>
				</td>
				<td>
					<span title="U+0294: LATIN LETTER GLOTTAL STOP" class='voiceless'>${segment_handler(request, u'ʔ', segments)}</span>
					<span class='voiced impossible'>&nbsp;</span>
				</td>
			</tr>
			<tr>
				<th class="manner">Nasal</th>
				<td>
					<span title="U+006D: LATIN SMALL LETTER M" class='voiced'>${segment_handler(request, u'm', segments)}</span>
				</td>
				<td>
					<span title="U+0271: LATIN SMALL LETTER M WITH HOOK" class='voiced'>${segment_handler(request, u'ɱ', segments)}</span>
				</td>
				<td>
                    <span title="U+006E-U+032A: LATIN SMALL LETTER N - COMBINING BRIDGE BELOW" class='voiced'>${segment_handler(request, u'n\u032a', segments)}</span>
                </td>
				<td>
					<span title="U+006E: LATIN SMALL LETTER N" class='voiced'>${segment_handler(request, u'n', segments)}</span>
				</td>
				<td></td>
				<td>
					<span title="U+0273: LATIN SMALL LETTER N WITH RETROFLEX HOOK" class='voiced'>${segment_handler(request, u'ɳ', segments)}</span>
				</td>
				<td>
					<span title="U+0272: LATIN SMALL LETTER N WITH LEFT HOOK" class='voiced'>${segment_handler(request, u'ɲ', segments)}</span>
				</td>
				<td>
					<span title="U+014B: LATIN SMALL LETTER ENG" class='voiced'>${segment_handler(request, u'ŋ', segments)}</span>
				</td>
				<td>
					<span title="U+0274: LATIN LETTER SMALL CAPITAL N" class='voiced'>${segment_handler(request, u'ɴ', segments)}</span>
				</td>
				<td class="impossible"></td>
				<td class="impossible"></td>
			</tr>
			<tr>
				<th class="manner">Trill</th>
				<td>
					<span title="U+0299: LATIN LETTER SMALL CAPITAL B" class='voiced'>${segment_handler(request, u'ʙ', segments)}</span>
				</td>
				<td></td>
				<td>
                    <span title="U+0072-U+032A: LATIN SMALL LETTER R - COMBINING BRIDGE BELOW" class='voiced'>${segment_handler(request, u'r\u032a', segments)}</span>
                </td>
				<td>
					<span title="U+0072: LATIN SMALL LETTER R" class='voiced'>${segment_handler(request, u'r', segments)}</span>
				</td>
				<td></td>
				<td></td>
				<td></td>
				<td class="impossible"></td>
				<td>
					<span title="U+0280: LATIN LETTER SMALL CAPITAL R" class='voiced'>${segment_handler(request, u'ʀ', segments)}</span>
				</td>
				<td></td>
				<td class="impossible"></td>
			</tr>
			<tr>
				<th class="manner">Tap or Flap</th>
				<td></td>
				<td>
					<span title="U+2C71: LATIN SMALL LETTER V WITH RIGHT HOOK" class='voiced'>${segment_handler(request, u'\u2C71', segments)}</span>
				</td>
				<td>
                    <span title="U+027E-U+032A: LATIN SMALL LETTER R WITH FISHHOOK - COMBINING BRIDGE BELOW" class='voiced'>${segment_handler(request, u'ɾ\u032a', segments)}</span>
                </td>
				<td>
					<span title="U+027E: LATIN SMALL LETTER R WITH FISHHOOK" class='voiced'>${segment_handler(request, u'ɾ', segments)}</span>
				</td>
				<td></td>
				<td>
					<span title="U+027D: LATIN SMALL LETTER R WITH TAIL" class='voiced'>${segment_handler(request, u'ɽ', segments)}</span>
				</td>
				<td></td>
				<td class="impossible"></td>
				<td></td>
				<td></td>
				<td class="impossible"></td>
			</tr>
			<tr>
				<th class="manner">Fricative</th>
				<td>
					<span title="U+0278: LATIN SMALL LETTER PHI" class='voiceless'>${segment_handler(request, u'ɸ', segments)}</span>
					<span title="U+03B2: GREEK SMALL LETTER BETA" class='voiced'>${segment_handler(request, u'β', segments)}</span>
				</td>
				<td>
					<span title="U+0066: LATIN SMALL LETTER F" class='voiceless'>${segment_handler(request, u'f', segments)}</span>
					<span title="U+0076: LATIN SMALL LETTER V" class='voiced'>${segment_handler(request, u'v', segments)}</span>
				</td>
				<td>
					<span title="U+03B8: GREEK SMALL LETTER THETA" class='voiceless'>${segment_handler(request, u'θ', segments)}</span>
					<span title="U+00F0: LATIN SMALL LETTER ETH" class='voiced'>${segment_handler(request, u'ð', segments)}</span>
				</td>
				<td>
					<span title="U+0073: LATIN SMALL LETTER S" class='voiceless'>${segment_handler(request, u's', segments)}</span>
					<span title="U+007A: LATIN SMALL LETTER Z" class='voiced'>${segment_handler(request, u'z', segments)}</span>
				</td>
				<td>
					<span title="U+0283: LATIN SMALL LETTER ESH" class='voiceless'>${segment_handler(request, u'ʃ', segments)}</span>
					<span title="U+0292: LATIN SMALL LETTER EZH" class='voiced'>${segment_handler(request, u'ʒ', segments)}</span>
				</td>
				<td>
					<span title="U+0282: LATIN SMALL LETTER S WITH HOOK" class='voiceless'>${segment_handler(request, u'ʂ', segments)}</span>
					<span title="U+0290: LATIN SMALL LETTER Z WITH RETROFLEX HOOK" class='voiced'>${segment_handler(request, u'ʐ', segments)}</span>
				</td>
				<td>
					<span title="U+00E7: LATIN SMALL LETTER C WITH CEDILLA" class='voiceless'>${segment_handler(request, u'ç', segments)}</span>
					<span title="U+029D: LATIN SMALL LETTER J WITH CROSSED-TAIL" class='voiced'>${segment_handler(request, u'ʝ', segments)}</span>
				</td>
				<td>
					<span title="U+0078: LATIN SMALL LETTER X" class='voiceless'>${segment_handler(request, u'x', segments)}</span>
					<span title="U+0263: LATIN SMALL LETTER GAMMA" class='voiced'>${segment_handler(request, u'ɣ', segments)}</span>
				</td>
				<td>
					<span title="U+03C7: GREEK SMALL LETTER CHI" class='voiceless'>${segment_handler(request, u'χ', segments)}</span>
					<span title="U+0281: LATIN LETTER SMALL CAPITAL INVERTED R" class='voiced'>${segment_handler(request, u'ʁ', segments)}</span>
				</td>
				<td>
					<span title="U+0127: LATIN SMALL LETTER H WITH STROKE" class='voiceless'>${segment_handler(request, u'ħ', segments)}</span>
					<span title="U+0295: LATIN LETTER PHARYNGEAL VOICED FRICATIVE" class='voiced'>${segment_handler(request, u'ʕ', segments)}</span>
				</td>
				<td>
					<span title="U+0068: LATIN SMALL LETTER H" class='voiceless'>${segment_handler(request, u'h', segments)}</span>
					<span title="U+0266: LATIN SMALL LETTER H WITH HOOK" class='voiced'>${segment_handler(request, u'ɦ', segments)}</span>
				</td>
			</tr>
			<tr>
				<th class="manner">Lateral fricative</th>
				<td class="impossible"></td>
				<td class="impossible"></td>
				<td></td>
				<td>
					<span title="U+026C: LATIN SMALL LETTER L WITH BELT" class='voiceless'>${segment_handler(request, u'ɬ', segments)}</span>
					<span title="U+026E: LATIN SMALL LETTER LEZH" class='voiced'>${segment_handler(request, u'ɮ', segments)}</span>
				</td>
				<td></td>
				<td></td>
				<td></td>
				<td></td>
				<td></td>
				<td class="impossible"></td>
				<td class="impossible"></td>
			</tr>
			<tr>
				<th class="manner">Approximant</th>
				<td></td>
				<td>
					<span title="U+028B: LATIN SMALL LETTER V WITH HOOK" class='voiced'>${segment_handler(request, u'ʋ', segments)}</span>
				</td>
				<td></td>
				<td>
					<span title="U+0279: LATIN SMALL LETTER TURNED R" class='voiced'>${segment_handler(request, u'ɹ', segments)}</span>
				</td>
				<td></td>
				<td>
					<span title="U+027B: LATIN SMALL LETTER TURNED R WITH HOOK" class='voiced'>${segment_handler(request, u'ɻ', segments)}</span>
				</td>
				<td>
					<span title="U+006A: LATIN SMALL LETTER J" class='voiced'>${segment_handler(request, u'j', segments)}</span>
				</td>
				<td>
					<span title="U+0270: LATIN SMALL LETTER TURNED M WITH LONG LEG" class='voiced'>${segment_handler(request, u'ɰ', segments)}</span>
				</td>
				<td></td>
				<td></td>
				<td class="impossible"></td>
			</tr>
			<tr>
				<th class="manner">Lateral approximant</th>
				<td class="impossible"></td>
				<td class="impossible"></td>
				<td>
                    <span title="U+006C-U+032A: LATIN SMALL LETTER L - COMBINING BRIDGE BELOW" class='voiced'>${segment_handler(request, u'l\u032a', segments)}</span>
                </td>
				<td>
					<span title="U+006C: LATIN SMALL LETTER L" class='voiced'>${segment_handler(request, u'l', segments)}</span>
				</td>
				<td></td>
				<td>
					<span title="U+026D: LATIN SMALL LETTER L WITH RETROFLEX HOOK" class='voiced'>${segment_handler(request, u'ɭ', segments)}</span>
				</td>
				<td>
					<span title="U+028E: LATIN SMALL LETTER TURNED Y" class='voiced'>${segment_handler(request, u'ʎ', segments)}</span>
				</td>
				<td>
					<span title="U+029F: LATIN LETTER SMALL CAPITAL L" class='voiced'>${segment_handler(request, u'ʟ', segments)}</span>
				</td>
				<td></td>
				<td class="impossible"></td>
				<td class="impossible"></td>
			</tr>
			</tbody>
		</table>
		<p>Where symbols appear in pairs, the one to the right represents a
		voiced consonant. Shaded areas denote articulations judged
		impossible.</p>
		</div>

		<div class="ipa" id="nonPulmonicConsonants">
		<h2>Consonants (Non-Pulmonic)</h2>
		<table>
			<colgroup span="2" />
			<colgroup span="2" />
			<colgroup span="2" />
			<thead>
				<tr>
					<th colspan="2">Clicks</th>
					<th colspan="2">Voiced implosives</th>
				</tr>
			</thead>
			<tbody>
				<tr>
					<td title="U+0298: LATIN LETTER BILABIAL CLICK">${segment_handler(request, u'ʘ', segments)}</td>
					<th>Bilabial</th>
					<td title="U+0253: LATIN SMALL LETTER B WITH HOOK">${segment_handler(request, u'ɓ', segments)}</td>
					<th>Bilabial</th>
				</tr>
				<tr>
					<td title="U+01C0: LATIN LETTER DENTAL CLICK">${segment_handler(request, u'ǀ', segments)}</td>
					<th>Dental</th>
					<td title="U+0257: LATIN SMALL LETTER D WITH HOOK">${segment_handler(request, u'ɗ', segments)}</td>
					<th>Dental/alveolar</th>
				</tr>
				<tr>
					<td title="U+01C3: LATIN LETTER RETROFLEX CLICK">${segment_handler(request, u'ǃ', segments)}</td>
					<th>(Post)alveolar</th>
					<td title="U+0284: LATIN SMALL LETTER DOTLESS J WITH STROKE AND HOOK">${segment_handler(request, u'ʄ', segments)}</td>
					<th>Palatal</th>
				</tr>
				<tr>
					<td title="U+01C2: LATIN LETTER ALVEOLAR CLICK">${segment_handler(request, u'ǂ', segments)}</td>
					<th>Palatoalveolar</th>
					<td title="U+0260: LATIN SMALL LETTER G WITH HOOK">${segment_handler(request, u'ɠ', segments)}</td>
					<th>Velar</th>
				</tr>
				<tr>
					<td title="U+01C1: LATIN LETTER LATERAL CLICK">${segment_handler(request, u'ǁ', segments)}</td>
					<th>Alveolar lateral</th>
					<td title="U+029B: LATIN LETTER SMALL CAPITAL G WITH HOOK">${segment_handler(request, u'ʛ', segments)}</td>
					<th>Uvular</th>
				</tr>
			</tbody>
		</table>
		</div>

		<div class="ipa" id="vowels">
		<h2>Vowels</h2>
		<div id="vowelQuadrilateral">
			<img id="vowelBackground" src="${request.static_url('phoible:static/vowelBackground.png')}" alt="Vowel Quadrilateral" />
			<div id="vowelLabels">
				<span style="right:76%; top:0">Front</span>
				<span style="right:40.5%; top:0">Central</span>
				<span style="right:3.5%; top:0">Back</span>

				<span style="left:-15px; top:11.21%">Close</span>
				<span style="left:-15px; top:36.48%">Close-mid</span>
				<span style="left:-15px; top:62.86%">Open-mid</span>
				<span style="left:-15px; top:89.23%">Open</span>
			</div>
			<div id="vowelSymbols">
				<div id="closeVowels">
                    <span title="U+0069-U+02d0: LATIN SMALL LETTER I - MODIFIER LETTER TRIANGULAR COLON" style="right:87.31%; top:11.21%;">${segment_handler(request, u'i\u02d0', segments, ns=True)}</span>
                    <span title="U+0069-U+0303: LATIN SMALL LETTER I - COMBINING TILDE" style="right:84.31%; top:11.21%;">${segment_handler(request, u'i\u0303', segments, ns=True)}</span>
					<span title="U+0069: LATIN SMALL LETTER I" style="right:81.31%; top:11.21%;">${segment_handler(request, u'i', segments)}</span>

                    <span title="U+0079: LATIN SMALL LETTER Y" style="right:74.77%; top:11.21%">${segment_handler(request, u'y', segments)}</span>
                    <span title="U+0079-U+0303: LATIN SMALL LETTER Y - COMBINING TILDE" style="right:71.77%; top:11.21%;">${segment_handler(request, u'y\u0303', segments, ns=True)}</span>
                    <span title="U+0079-U+02d0: LATIN SMALL LETTER Y - MODIFIER LETTER TRIANGULAR COLON" style="right:68.77%; top:11.21%;">${segment_handler(request, u'y\u02d0', segments, ns=True)}</span>

                    <span title="U+0268-U+02d0: LATIN SMALL LETTER I WITH STROKE - MODIFIER LETTER TRIANGULAR COLON" style="right:48%; top:11.21%;">${segment_handler(request, u'ɨ\u02d0', segments, ns=True)}</span>
                    <span title="U+0268-U+0303: LATIN SMALL LETTER I WITH STROKE - COMBINING TILDE" style="right:46%; top:11.21%;">${segment_handler(request, u'ɨ\u0303', segments, ns=True)}</span>
					<span title="U+0268: LATIN SMALL LETTER I WITH STROKE" style="right:44%; top:11.21%">${segment_handler(request, u'ɨ', segments)}</span>

					<span title="U+0289: LATIN SMALL LETTER U BAR" style="right:36.5%; top:11.21%">${segment_handler(request, u'ʉ', segments)}</span>
                    <span title="U+0289-U+0303: LATIN SMALL LETTER U BAR - COMBINING TILDE" style="right:33.5%; top:11.21%;">${segment_handler(request, u'ʉ\u0303', segments, ns=True)}</span>
                    <span title="U+0289-U+02d0: LATIN SMALL LETTER U BAR - MODIFIER LETTER TRIANGULAR COLON" style="right:30.5%; top:11.21%;">${segment_handler(request, u'ʉ\u02d0', segments, ns=True)}</span>

                    <span title="U+006F-U+02d0: LATIN SMALL LETTER TURNED M - MODIFIER LETTER TRIANGULAR COLON" style="right:12%; top:11.21%;">${segment_handler(request, u'ɯ\u02d0', segments, ns=True)}</span>
                    <span title="U+006F-U+0303: LATIN SMALL LETTER TURNED M - COMBINING TILDE" style="right:10%; top:11.21%;">${segment_handler(request, u'ɯ\u0303', segments, ns=True)}</span>
					<span title="U+026F: LATIN SMALL LETTER TURNED M" style="right:8.00%; top:11.21%">${segment_handler(request, u'ɯ', segments)}</span>

					<span title="U+0075: LATIN SMALL LETTER U" style="right:2%; top:11.21%">${segment_handler(request, u'u', segments)}</span>
                    <span title="U+0075-U+0303: LATIN SMALL LETTER U - COMBINING TILDE" style="right:-2%; top:11.21%;">${segment_handler(request, u'u\u0303', segments, ns=True)}</span>
                    <span title="U+0075-U+02d0: LATIN SMALL LETTER U - MODIFIER LETTER TRIANGULAR COLON" style="right:-6%; top:11.21%;">${segment_handler(request, u'u\u02d0', segments, ns=True)}</span>
				</div>
				<div id="closeLaxVowels">
                    <span title="U+026A-U+02d0: LATIN SMALL LETTER CAPITAL I - MODIFIER LETTER TRIANGULAR COLON" style="right:68%; top:22.90%;">${segment_handler(request, u'ɪ\u02d0', segments, ns=True)}</span>
                    <span title="U+026A-U+0303: LATIN SMALL LETTER CAPITAL I - COMBINING TILDE" style="right:65%; top:22.90%;">${segment_handler(request, u'ɪ\u0303', segments, ns=True)}</span>
					<span title="U+026A: LATIN LETTER SMALL CAPITAL I" style="right:62%; top:22.90%">${segment_handler(request, u'ɪ', segments)}</span>

                    <span title="U+028F: LATIN LETTER SMALL CAPITAL Y" style="right:56%; top:22.90%">${segment_handler(request, u'ʏ', segments)}</span>
                    <!-- no variants for LATIN LETTER SMALL CAPITAL Y -->

					<span title="U+028A: LATIN SMALL LETTER UPSILON" style="right:19.5%; top:22.90%">${segment_handler(request, u'ʊ', segments)}</span>
                    <span title="U+028A-U+0303: LATIN SMALL LETTER UPSILON - COMBINING TILDE" style="right:16%; top:22.90%;">${segment_handler(request, u'ʊ\u0303', segments, ns=True)}</span>
                    <span title="U+028A-U+02d0: LATIN SMALL LETTER UPSILON - MODIFIER LETTER TRIANGULAR COLON" style="right:12.5%; top:22.90%;">${segment_handler(request, u'ʊ\u02d0', segments, ns=True)}</span>
				</div>
				<div id="close-midVowels">
                    <span title="U+0065-U+02d0: LATIN SMALL LETTER E - MODIFIER LETTER TRIANGULAR COLON" style="right:76.85%; top:36.48%;">${segment_handler(request, u'e\u02d0', segments, ns=True)}</span>
                    <span title="U+0065-U+0303: LATIN SMALL LETTER E - COMBINING TILDE" style="right:73.85%; top:36.48%;">${segment_handler(request, u'e\u0303', segments, ns=True)}</span>
					<span title="U+0065: LATIN SMALL LETTER E" style="right:70.85%; top:36.48%">${segment_handler(request, u'e', segments)}</span>

                    <span title="U+00F8: LATIN SMALL LETTER O WITH STROKE" style="right:63%; top:36.48%">${segment_handler(request, u'ø', segments)}</span>
                    <span title="U+00F8-U+0303: LATIN SMALL LETTER O WITH STROKE - COMBINING TILDE" style="right:60.5%; top:36.48%;">${segment_handler(request, u'ø\u0303', segments, ns=True)}</span>
                    <span title="U+00F8-U+02d0: LATIN SMALL LETTER O WITH STROKE - MODIFIER LETTER TRIANGULAR COLON" style="right:58%; top:36.48%;">${segment_handler(request, u'ø\u02d0', segments, ns=True)}</span>

                    <span title="U+0258-U+02d0: LATIN SMALL LETTER REVERSED E - MODIFIER LETTER TRIANGULAR COLON" style="right:43%; top:36.48%;">${segment_handler(request, u'ɘ\u02d0', segments, ns=True)}</span>
                    <span title="U+0258-U+0303: LATIN SMALL LETTER REVERSED E - COMBINING TILDE" style="right:41%; top:36.48%;">${segment_handler(request, u'ɘ\u0303', segments, ns=True)}</span>
					<span title="U+0258: LATIN SMALL LETTER REVERSED E" style="right:39%; top:36.48%">${segment_handler(request, u'ɘ', segments)}</span>

					<span title="U+0275: LATIN SMALL LETTER BARRED O" style="right:31%; top:36.48%">${segment_handler(request, u'ɵ', segments)}</span>
                    <span title="U+0275-U+0303: LATIN SMALL LETTER BARRED O - COMBINING TILDE" style="right:28%; top:36.48%;">${segment_handler(request, u'ɵ\u0303', segments, ns=True)}</span>
                    <span title="U+0275-U+02d0: LATIN SMALL LETTER BARRED O - MODIFIER LETTER TRIANGULAR COLON" style="right:25%; top:36.48%;">${segment_handler(request, u'ɵ\u02d0', segments, ns=True)}</span>

                    <span title="U+0264-U+02d0: LATIN SMALL LETTER RAMS HORN - MODIFIER LETTER TRIANGULAR COLON" style="right:12%; top:36.48%;">${segment_handler(request, u'ɤ\u02d0', segments, ns=True)}</span>
                    <span title="U+0264-U+0303: LATIN SMALL LETTER RAMS HORN - COMBINING TILDE" style="right:10%; top:36.48%;">${segment_handler(request, u'ɤ\u0303', segments, ns=True)}</span>
					<span title="U+0264: LATIN SMALL LETTER RAMS HORN" style="right:8.00%; top:36.48%">${segment_handler(request, u'ɤ', segments)}</span>

					<span title="U+006F: LATIN SMALL LETTER O" style="right:2%; top:36.48%">${segment_handler(request, u'o', segments)}</span>
                    <span title="U+006F-U+0303: LATIN SMALL LETTER O - COMBINING TILDE" style="right:-2%; top:36.48%;">${segment_handler(request, u'o\u0303', segments, ns=True)}</span>
                    <span title="U+006F-U+02d0: LATIN SMALL LETTER O - MODIFIER LETTER TRIANGULAR COLON" style="right:-6%; top:36.48%;">${segment_handler(request, u'o\u02d0', segments, ns=True)}</span>
				</div>
				<div id="middleVowels">
                    <span title="U+006F-U+0303: LATIN SMALL LETTER SCHWA - COMBINING TILDE" style="right:37%; top:49.27%;">${segment_handler(request, u'ə\u0303', segments, ns=True)}</span>
					<span title="U+0259: LATIN SMALL LETTER SCHWA" style="right:33%; top:49.27%">${segment_handler(request, u'ə', segments)}</span>
                    <span title="U+006F-U+02d0: LATIN SMALL LETTER SCHWA - MODIFIER LETTER TRIANGULAR COLON" style="right:27%; top:49.27%;">${segment_handler(request, u'ə\u02d0', segments, ns=True)}</span>
				</div>
				<div id="open-midVowels">
                    <span title="U+025B-U+02d0: LATIN SMALL LETTER OPEN E - MODIFIER LETTER TRIANGULAR COLON" style="right:64%; top:62.90%;">${segment_handler(request, u'ɛ\u02d0', segments, ns=True)}</span>
                    <span title="U+025B-U+0303: LATIN SMALL LETTER OPEN E - COMBINING TILDE" style="right:61%; top:62.90%;">${segment_handler(request, u'ɛ\u0303', segments, ns=True)}</span>
					<span title="U+025B: LATIN SMALL LETTER OPEN E" style="right:58%; top:62.90%">${segment_handler(request, u'ɛ', segments)}</span>

                    <span title="U+0153: LATIN SMALL LIGATURE OE" style="right:50%; top:62.90%">${segment_handler(request, u'œ', segments)}</span>
                    <span title="U+0153-U+0303: LATIN SMALL LIGATURE OE - COMBINING TILDE" style="right:47%; top:62.90%;">${segment_handler(request, u'œ\u0303', segments, ns=True)}</span>
                    <span title="U+0153-U+02d0: LATIN SMALL LIGATURE OE - MODIFIER LETTER TRIANGULAR COLON" style="right:44%; top:62.90%;">${segment_handler(request, u'œ\u02d0', segments, ns=True)}</span>

                    <span title="U+025C-U+02d0: LATIN SMALL LETTER REVERSED OPEN E - MODIFIER LETTER TRIANGULAR COLON" style="right:37%; top:62.90%;">${segment_handler(request, u'ɜ\u02d0', segments, ns=True)}</span>
                    <span title="U+025C-U+0303: LATIN SMALL LETTER REVERSED OPEN E - COMBINING TILDE" style="right:35%; top:62.90%;">${segment_handler(request, u'ɜ\u0303', segments, ns=True)}</span>
					<span title="U+025C: LATIN SMALL LETTER REVERSED OPEN E" style="right:33%; top:62.90%">${segment_handler(request, u'ɜ', segments)}</span>

					<span title="U+025E: LATIN SMALL LETTER CLOSED REVERSED OPEN E" style="right:24.15%; top:62.90%">${segment_handler(request, u'ɞ', segments)}</span>
                    <!-- no variants known -->

                    <span title="U+028C-U+0303: LATIN SMALL LETTER TURNED V - MODIFIER LETTER TRIANGULAR COLON" style="right:12%; top:62.90%">${segment_handler(request, u'ʌ\u02d0', segments, ns=True)}</span>
                    <span title="U+028C-U+0303: LATIN SMALL LETTER TURNED V - COMBINING TILDE" style="right:10%; top:62.90%;">${segment_handler(request, u'ʌ\u0303', segments, ns=True)}</span>
					<span title="U+028C: LATIN SMALL LETTER TURNED V" style="right:8.00%; top:62.90%">${segment_handler(request, u'ʌ', segments)}</span>

					<span title="U+0254: LATIN SMALL LETTER OPEN O" style="right:2%; top:62.90%">${segment_handler(request, u'ɔ', segments)}</span>
                    <span title="U+0254-U+0303: LATIN SMALL LETTER OPEN O - COMBINING TILDE" style="right:-2%; top:62.90%;">${segment_handler(request, u'ɔ\u0303', segments, ns=True)}</span>
                    <span title="U+0254-U+02d0: LATIN SMALL LETTER OPEN O - MODIFIER LETTER TRIANGULAR COLON" style="right:-6%; top:62.90%;">${segment_handler(request, u'ɔ\u02d0', segments, ns=True)}</span>
				</div>
				<div id="openLaxVowels">
                    <span title="U+00E6-U+02d0: LATIN SMALL LETTER AE - MODIFIER LETTER TRIANGULAR COLON" style="right:56.23%; top:77.41%;">${segment_handler(request, u'æ\u02d0', segments, ns=True)}</span>
                    <span title="U+00E6-U+0303: LATIN SMALL LETTER AE - COMBINING TILDE" style="right:53.23%; top:77.41%;">${segment_handler(request, u'æ\u0303', segments, ns=True)}</span>
					<span title="U+00E6: LATIN SMALL LETTER AE" style="right:50.23%; top:77.41%">${segment_handler(request, u'æ', segments)}</span>

                    <span title="U+0250-U+0303: LATIN SMALL LETTER TURNED A - COMBINING TILDE" style="right:30.5%; top:75.65%;">${segment_handler(request, u'ɐ\u0303', segments, ns=True)}</span>
					<span title="U+0250: LATIN SMALL LETTER TURNED A" style="right:26.5%; top:75.65%">${segment_handler(request, u'ɐ', segments)}</span>
                    <span title="U+0250-U+02d0: LATIN SMALL LETTER TURNED A - MODIFIER LETTER TRIANGULAR COLON" style="right:22.5%; top:75.65%;">${segment_handler(request, u'ɐ\u02d0', segments, ns=True)}</span>
				</div>
				<div id="openVowels">
                    <span title="U+0061-U+02d0: LATIN SMALL LETTER A - MODIFIER LETTER TRIANGULAR COLON" style="right:50.23%; top:89.84%;">${segment_handler(request, u'a\u02d0', segments, ns=True)}</span>
                    <span title="U+0061-U+0303: LATIN SMALL LETTER A - COMBINING TILDE" style="right:47.23%; top:89.84%;">${segment_handler(request, u'a\u0303', segments, ns=True)}</span>
					<span title="U+0061: LATIN SMALL LETTER A" style="right:44.23%; top:89.84%">${segment_handler(request, u'a', segments)}</span>

                    <span title="U+0276: LATIN LETTER SMALL CAPITAL OE" style="right:37%; top:89.84%">${segment_handler(request, u'ɶ', segments)}</span>
                    <span title="U+0276-U+: LATIN LETTER SMALL CAPITAL OE - COMBINING UP TACK BELOW" style="right:33%; top:89.84%">${segment_handler(request, u'ɶ̝', segments, ns=True)}</span>

                    <span title="U+0251-U+02d0: LATIN SMALL LETTER ALPHA - MODIFIER LETTER TRIANGULAR COLON" style="right:12%; top:89.84%;">${segment_handler(request, u'ɑ\u02d0', segments, ns=True)}</span>
                    <span title="U+0251-U+0303: LATIN SMALL LETTER ALPHA - COMBINING TILDE" style="right:10%; top:89.84%;">${segment_handler(request, u'ɑ\u0303', segments, ns=True)}</span>
					<span title="U+0251: LATIN SMALL LETTER ALPHA" style="right:8.00%; top:89.84%">${segment_handler(request, u'ɑ', segments)}</span>

					<span title="U+0252: LATIN SMALL LETTER TURNED ALPHA" style="right:2%; top:89.84%">${segment_handler(request, u'ɒ', segments)}</span>
                    <span title="U+0252-U+0303: LATIN SMALL LETTER TURNED ALPHA - COMBINING TILDE" style="right:-2%; top:89.84%;">${segment_handler(request, u'ɒ\u0303', segments, ns=True)}</span>
                    <span title="U+0252-U+02d0: LATIN SMALL LETTER TURNED ALPHA - MODIFIER LETTER TRIANGULAR COLON" style="right:-6%; top:89.84%;">${segment_handler(request, u'ɒ\u02d0', segments, ns=True)}</span>
				</div>
			</div>
		</div>
		<p class='caption'>Where symbols appear in pairs, the one to the right represents a rounded vowel.</p>
		</div>
        % if segments:
		<div class="ipa" id="otherSymbols">
		<h2>Other Segments</h2>
            <table>
                <tbody>
                % for segment in segments.values():
                <tr>
                    <td>${h.link(request, segment)}</td>
                    <td style="font-size: smaller;">${segment.description}</td>
                </tr>
                % endfor
                </tbody>
             </table>
		</div>
        % endif
</%def>
