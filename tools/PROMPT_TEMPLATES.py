# Paws & Prejudice — PROMPT TEMPLATES
# Every render must use these prefixes/suffixes. No exceptions.

PROMPT_PREFIX = """PHOTOREALISTIC. 35mm film aesthetic with subtle grain. Vintage period drama cinematography. Film-like color grading. NOT cartoon. NOT animation. NOT illustration. NOT stylized. NOT digital art. Realistic fur textures."""

BIPEDAL_RULE = """CRITICAL ANATOMY RULE: Every character is an ANTHROPOMORPHIC ANIMAL standing UPRIGHT on TWO LEGS like a human. BIPEDAL. They walk, stand, gesture, and move on their HIND LEGS exactly like humans in period costume. They have human-like posture and body language. They are NOT regular dogs on all fours. They are NOT quadrupeds. They are upright, bipedal, anthropomorphic characters who happen to have dog or cat features."""

NO_TEXT_RULE = """CRITICAL: ENGLISH ONLY. NO Chinese characters. NO Japanese. NO Korean. NO text of any kind anywhere in the video. NO subtitles. NO captions. NO watermarks. NO letters. NO words. ABSOLUTELY NO TEXT ON SCREEN."""

VINTAGE_FILM_SUFFIX = """VINTAGE FILM EFFECT: Subtle 35mm film grain throughout. Slight warm amber color shift. Soft vignette at frame edges. Gentle flicker like aged film stock. Muted contrast with lifted blacks. Slight halation around bright light sources. The look of 1970s BBC period drama shot on 16mm. Warm, nostalgic, slightly imperfect. Like watching Pride and Prejudice on a well-loved VHS tape. Dust specks and subtle film weave. NOT digitally clean. NOT modern sharp digital video. The footage should feel like it was discovered in an archive, not rendered yesterday."""

# Combine for full prompt:
# FULL_PROMPT = f"{PROMPT_PREFIX}\n\n{BIPEDAL_RULE}\n\n{NO_TEXT_RULE}\n\n[EPISODE-SPECIFIC PROMPT]\n\n{VINTAGE_FILM_SUFFIX}"
