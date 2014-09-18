# -*- coding: utf-8 -*-

import discog
import mwsiteext

site = mwsiteext.Site()

def test(test_func):
    band, expected = test_func()
    
    album_page_names = discog.parse_discog_section(site, band, "Discography")
    for expected_name in expected[:]:
        if expected_name in album_page_names:
            album_page_names.remove(expected_name)
            expected.remove(expected_name)
    
    print "{0} RESULT".format(band)
    
    if expected:
        print "Did not find the following expected pages:"
        for expected_name in expected:
            print expected_name
        print
    
    if album_page_names:
        print "Found the following unexpected pages:"
        for album_page_name in album_page_names:
            print album_page_name
    
    if not expected and not album_page_names:
        print "SUCCESS"
    
    print

def curve():
    albums = [u"Doppelgänger (Curve album)", "Cuckoo (album)", "Come Clean (Curve album)", "Gift (Curve album)", "The New Adventures of Curve"]
    compilations = ["Pubic Fruit", "Radio Sessions", "Open Day at the Hate Fest", "The Way of Curve", "Rare and Unreleased (Curve album)"]
    eps_singles = ["Blindfold (EP)", "Frozen (EP)", "Cherry (EP)", u"Faît Accompli (Curve song)", "Horror Head", "Blackerthreetracker", "Superblaster",
                   "Pink Girl With the Blues", "Chinese Burn (song)", "Coming Up Roses (song)", "Perish (song)", "Want More Need Less"]
    one_off = ["I Feel Love"]
    return "Curve (band)", albums + compilations + eps_singles + one_off

def red_sparowes():
    albums = ["At the Soundless Dawn", "Every Red Heart Shines Toward the Red Sun", "The Fear Is Excruciating, But Therein Lies the Answer"]
    other = ["Gregor Samsa (band)", "Oh Lord, God of Vengeance, Show Yourself!", "Aphorisms (album)"]
    return "Red Sparowes", albums + other

test(curve)
test(red_sparowes)
# band, expected = "Depswa", []		# I currently feel this style discog section is too unique to handle

