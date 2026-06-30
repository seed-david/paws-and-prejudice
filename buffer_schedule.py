#!/usr/bin/env python3
"""
Paws & Prejudice - Buffer Scheduling Script
450 episodes, 3 channels each = 1350 API calls
5 episodes per day starting 2026-03-30 at 18:00 BST
"""

import json
import requests
import time
import sys
from datetime import datetime, timedelta, timezone
import os

# Buffer API config
API_KEY = "KBfzqAH12FOIaDVDBKXiwvwGqy7VfiY8Z4g18Jg5z7k"
GRAPHQL_URL = "https://api.buffer.com/graphql"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

ORG_ID = "69c9361222df31cc73efe06b"

CHANNELS = {
    "tiktok": "69c93709af47dacb6968ed1e",
    "instagram": "69c938a8af47dacb6968f24e",
    "youtube": "69c93cb5af47dacb6968fd00",
}

HASHTAGS_SOCIAL = "#PawsAndPrejudice #PrideAndPrejudice #viral #cats #dogs #animalsaddict #catlover #doglovers"
HASHTAGS_YOUTUBE = "#PawsAndPrejudice #PrideAndPrejudice #AIAnimation"

SEASON_NAMES = {
    1: "The Arrival",
    2: "The Entanglement",
    3: "The Collapse",
    4: "The Reckoning",
    5: "The Resolution",
}

# ─────────────────────────────────────────────────────────────────────────────
# EPISODE DATA — all 420 episodes with loglines
# ─────────────────────────────────────────────────────────────────────────────

EPISODES = [
    # ── SEASON 1: THE ARRIVAL ────────────────────────────────────────────────
    (1, 1, "FIRST INTELLIGENCE", "Lady Woofington-Barks has received intelligence. She cannot breathe."),
    (1, 2, "THE HOUSEHOLD ASSEMBLED", "The whole family assembled. Only one of them is useful."),
    (1, 3, "THE BONNET COUNCIL", "She is wearing three bonnets. She needs four. This is war."),
    (1, 4, "LORD BISCUIT-BOTTOMS COMMENTS", "He has survived thirty years of marriage. Just."),
    (1, 5, "ELIZA'S POSITION", "She refuses to love a cat she has never met. History disagrees."),
    (1, 6, "JANE HOPES", "Jane hopes. Eliza worries. This is their entire relationship."),
    (1, 7, "LYDIA HAS PLANS", "Lydia has decided he is handsome. She has not met him."),
    (1, 8, "KITTY FOLLOWS", "Kitty chose the sensible path for four seconds. Then did not."),
    (1, 9, "MARY HAS THOUGHTS", "Mary delivered a philosophical observation. No one heard it."),
    (1, 10, "THE BONNET PURCHASE", "The bonnet was an investment. In what, precisely, is unclear."),
    (1, 11, "LORD BISCUIT-BOTTOMS NOTICES", "The bill arrived. The eyebrow rose. The page was turned."),
    (1, 12, "HORTENSIA BROADCASTS", "She is not a gossip. She is an intelligence network with a fan."),
    (1, 13, "THE HUFFINGTON-SCRATCHES REACT", "Seven daughters. The mathematics are in their favour."),
    (1, 14, "ZELDA'S FIRST CARDS", "She saw everything. No one asked. Naturally."),
    (1, 15, "THE ESTATE LIGHTS UP", "The candles are new. The cats are coming. Nobody is prepared."),
    (1, 16, "THE CATS ARRIVE", "One waved. One stared. One found everything below consideration."),
    (1, 17, "FIRST IMPRESSIONS: BINGLEY", "His tail wagged. In the cat community, this is remarkable."),
    (1, 18, "FIRST IMPRESSIONS: DARCY", "One eyebrow. One sweep of the county. One verdict."),
    (1, 19, "FIRST IMPRESSIONS: CAROLINE", "She smiled at everything. Nothing improved from the experience."),
    (1, 20, "THE BALL IS ANNOUNCED", "The bonnet was, retrospectively, a bargain."),
    (1, 21, "FIVE DAUGHTERS, FIVE GOWNS", "One afternoon. Multiple fabric emergencies. Lord B-B retreats."),
    (1, 22, "MARY PREPARES A PIECE", "She has been practising for three weeks. They have been grieving for two."),
    (1, 23, "LYDIA PREPARES A STRATEGY", "Three officers, no plan whatsoever. Kitty recruited. Not consulted."),
    (1, 24, "THE CARRIAGE SITUATION", "Seven Fetchworths, six seats. Mathematics was attempted. Mathematics lost."),
    (1, 25, "ARRIVAL AT THE ASSEMBLY", "Lady Woofington-Barks had rehearsed this entrance. It showed."),
    (1, 26, "THE ROOM REACTS", "Both sides found cause for alarm and blamed the candelabras."),
    (1, 27, "BINGLEY SEES JANE", "His tail went vertical. Three parishes witnessed it."),
    (1, 28, "DARCY ASSESSES", "He found the room insufficient. He found his wall. He stayed."),
    (1, 29, "THE FIRST DANCE: BINGLEY AND JANE", "He asked. She blushed completely. Lady W-B's plan was working."),
    (1, 30, "DARCY DECLINES", "Bingley suggested dancing. One eyebrow. One word. No dancing."),
    (1, 31, "THE ELIZA OBSERVATION", "He said it six feet from the Border Collie in question."),
    (1, 32, "ELIZA'S RESPONSE", "She turned an insult into the best story at the Assembly."),
    (1, 33, "LADY W-B ON BINGLEY", "He danced with her twice. That is practically an engagement."),
    (1, 34, "LORD BISCUIT-BOTTOMS ON LOVE", "Clear love and declared love are separated by considerable suffering."),
    (1, 35, "CAROLINE WATCHES", "She watched Bingley watch Jane and revised her strategy entirely."),
    (1, 36, "WICKHAM IS SPOTTED", "A Siamese in military uniform. Lydia saw him first. Too late for everyone."),
    (1, 37, "THE REGIMENT ARRIVES", "Lydia deployed herself into the High Street. No tactics were used."),
    (1, 38, "MARY PERFORMS", "The notes were confident. The room thinned. Barksworth wept."),
    (1, 39, "THE EVENING'S VERDICT", "Jane: triumph. Bingley: secured. Bonnet: vindicated."),
    (1, 40, "DARCY'S PRIVATE MOMENT", "An askew bonnet. A sharp laugh. He found this extremely irritating."),
    (1, 41, "THE NETHERFIELD BALL ANNOUNCED", "A proper ball. At the actual house. This is not a drill."),
    (1, 42, "PREPARATIONS BEGIN", "Lord Biscuit-Bottoms found a quieter wing. Then a further one."),
    (1, 43, "CHARLOTTE'S COUNSEL", "Smile at the ones with money. Eliza would rather eat her bonnet."),
    (1, 44, "JANE'S HOPE", "She would not presume. She would simply hope, which is worse."),
    (1, 45, "THE ARRIVAL AT NETHERFIELD", "Caroline smiled down from the stairs. Neither side blinked."),
    (1, 46, "MRS WOOFSLEY CRASHES", "Uninvited, unapologetic, nine Pugs. The butler had no protocol."),
    (1, 47, "THE NINE PUGS", "Gerald was already under the refreshment table. Gerald understood priorities."),
    (1, 48, "GASTON PREPARES THE DINNER", "Both the soup and the commentary would be served cold."),
    (1, 49, "BINGLEY AND JANE: THE SECOND DANCE", "He asked immediately. She blushed completely. Again. Pattern confirmed."),
    (1, 50, "DARCY AND ELIZA DANCE", "He asked. She accepted. Both were surprised. The waltz required no explanation."),
    (1, 51, "THE DANCING ARGUMENT", "They argued through the waltz while remaining formally correct."),
    (1, 52, "WICKHAM'S ABSENCE", "The evening became a surveillance operation conducted through eyebrows."),
    (1, 53, "COLLINS ARRIVES", "He bowed to the doorframe. He bowed to the chair. He was not invited."),
    (1, 54, "COLLINS GREETS DARCY", "The eyebrow achieved heights from which no eyebrow has returned."),
    (1, 55, "LADY W-B MONITORS", "She tracked the Bingley-Jane orbital pattern. None of the subtlety."),
    (1, 56, "LORD BISCUIT-BOTTOMS AT THE CARD TABLE", "He won steadily and remained gloriously uninvolved."),
    (1, 57, "GASTON SERVES THE SOUP", "The ginger one is in love. The dark one is in love and furious."),
    (1, 58, "LYDIA AND THE REGIMENT", "She was conducting parallel conversations with telegraph efficiency."),
    (1, 59, "KITTY ATTEMPTS TO MODERATE", "She tried twice. She failed twice. She took a glass of punch."),
    (1, 60, "MARY AT THE PIANOFORTE", "The room braced. The notes arrived. The room thinned."),
    (1, 61, "PROFESSOR BARKSWORTH IS PRESENT", "He is ready. He has a notebook. He is the only one."),
    (1, 62, "MARY PERFORMS AT THE BALL", "Barksworth transcended. The woman beside him had her fingers in her ears."),
    (1, 63, "LORD BISCUIT-BOTTOMS ENDS IT", "One sentence. Quietly. Absolutely final. The room exhaled."),
    (1, 64, "LADY W-B'S ANNOUNCEMENT", "She announced the engagement publicly. This was catastrophic immediately."),
    (1, 65, "DARCY HEARS THIS", "He filed it under concerns. Caroline filed it under opportunities."),
    (1, 66, "JANE'S MORTIFICATION", "She turned crimson. Bingley was not embarrassed at all. Worse."),
    (1, 67, "ELIZA AND THE EVENING'S END", "One dance unplanned, one argument won, one absent Siamese."),
    (1, 68, "THE CARRIAGE HOME", "Eliza watched the countryside and replayed one particular waltz."),
    (1, 69, "DARCY'S SECOND PRIVATE MOMENT", "The Border Collie was becoming increasingly inconvenient."),
    (1, 70, "CAROLINE'S LETTER", "Warm words. Elegant script. A name quietly, elegantly erased."),
    (1, 71, "JANE GETS WET", "Lady W-B sent Jane on horseback. In rain. The plan was transparent."),
    (1, 72, "THE PLAN WORKS TOO WELL", "Jane arrived soaked, feverish, charming about it. Lady W-B: satisfied."),
    (1, 73, "ELIZA WALKS OVER", "Three miles. Mud. Hedgerows. She did not care what anyone thought of her hem."),
    (1, 74, "CAROLINE'S FACE", "The smile surveyed the muddy hem and found a comprehensive argument."),
    (1, 75, "DARCY OBSERVES THE ARRIVAL", "He did not mind the mud. He minded that he did not mind it."),
    (1, 76, "ELIZA NURSES JANE", "She would fight a ballroom for this retriever."),
    (1, 77, "THE NETHERFIELD BREAKFAST", "The toast had never been more interesting. Caroline disagreed."),
    (1, 78, "CAROLINE ON ELIZA", "Each compliment was a scalpel. Eliza received them with amusement."),
    (1, 79, "DARCY READS", "The book had been on the same page for four minutes. He had not noticed."),
    (1, 80, "THE LIBRARY CONVERSATION", "Two intelligent creatures, briefly, speaking the same language."),
    (1, 81, "CAROLINE WALKS", "She walked for him to notice. He noticed Eliza instead."),
    (1, 82, "JANE IMPROVES", "She was recovering, which Lady W-B found mildly disappointing."),
    (1, 83, "LADY W-B AT NETHERFIELD", "She mentioned the wedding. She departed. A look was exchanged."),
    (1, 84, "CAROLINE'S CAMPAIGN", "She told him about the engagement rumour. His voice was not steady."),
    (1, 85, "JANE LEAVES NETHERFIELD", "Bingley said farewell in twelve separate expressions of hope."),
    (1, 86, "CAROLINE'S LETTER TO JANE", "The warmth concealed blades. A masterpiece of destruction as friendship."),
    (1, 87, "JANE READS THE LETTER", "Jane found the best interpretation. Eliza found the real one."),
    (1, 88, "ELIZA'S ASSESSMENT", "Eliza told Jane what the letter meant. Jane disagreed. Both were sad."),
    (1, 89, "DARCY'S RESOLUTION", "He resolved to master his feelings. His reflection was unconvinced."),
    (1, 90, "THE SEASON TURNS", "A proud cat was losing a fight with his feelings. She was pretending not to notice."),

    # ── SEASON 2: THE ENTANGLEMENT ───────────────────────────────────────────
    (2, 91, "THE INTRODUCTION", "He introduced himself. His smile was exactly the right width. Almost."),
    (2, 92, "THE DARCY ENCOUNTER", "An entire history passed between them in two seconds."),
    (2, 93, "WICKHAM'S STORY BEGINS", "He began his story the way all accomplished liars do: with a truth."),
    (2, 94, "THE INHERITANCE TALE", "Specific. Plausible. A masterwork of fiction from whisker to tail-tip."),
    (2, 95, "ELIZA BELIEVES HIM", "She believed him. She had already written the verdict."),
    (2, 96, "THE STORY SPREADS", "By supper it was county fact. Accuracy was no longer the point."),
    (2, 97, "DARCY HEARS THE RUMOURS", "He received the slander with the emotional range of a closed door."),
    (2, 98, "COLONEL FITZWILLIAM ARRIVES", "He had already complimented four bonnets. Darcy closed his eyes."),
    (2, 99, "FITZWILLIAM MEETS THE FETCHWORTH FAMILY", "He accidentally revealed three private matters in eight minutes."),
    (2, 100, "LYDIA AND THE REGIMENT", "A match at a fireworks display: magnificent, inevitable, unsupervised."),
    (2, 101, "SERGEANT RUFFINGTON TRIES", "The warning ricocheted off two Fetchworth daughters and fell wounded."),
    (2, 102, "AUNT GARDINER VISITS", "She brought common sense, good shoes, and the county's only functioning adult."),
    (2, 103, "AUNT GARDINER'S WARNING", "Questions, one after another, each a polite detonation."),
    (2, 104, "WICKHAM PIVOTS", "His affections were portable and had found a better postcode."),
    (2, 105, "ELIZA'S PRIDE", "She was not heartbroken. She was beginning to suspect she was wrong."),
    (2, 106, "LORD VELVETTHORN SEEN", "A stranger arrives. Zelda draws the Tower card before he has unpacked."),
    (2, 107, "THE CHRISTMAS PREPARATIONS", "Lady W-B's list has seventeen items. Lydia immediately mentions the regiment."),
    (2, 108, "DARCY AT A DISTANCE", "He rode past her house. The horse knew the route. The horse was not asked."),
    (2, 109, "CAROLINE'S TRIUMPH LETTER", "A masterclass in saying absolutely nothing while saying everything."),
    (2, 110, "JANE'S QUIET GRIEF", "Her grief was so quiet it could only be heard by a sister."),
    (2, 111, "WICKHAM'S FAREWELL", "He distributed farewells with pre-prepared efficiency."),
    (2, 112, "HIS PARTING WORDS TO ELIZA", "Either a goodbye or an investment. She could not tell which."),
    (2, 113, "LORD VELVETTHORN AT THE ASSEMBLY", "Present, silent, making everyone slightly uneasy."),
    (2, 114, "ZELDA APPROACHES VELVETTHORN", "She had already read his future. He declined. She nodded."),
    (2, 115, "THE YEAR'S END", "A tuxedo cat on a cold road, watching a window he had no business watching."),
    (2, 116, "THE LETTER ARRIVES", "Four paragraphs longer than the information required. Collins is coming."),
    (2, 117, "THE COLLINS LETTER READ ALOUD", "Eleven mentions of Lady Catherine. Lord Biscuit-Bottoms is savouring this."),
    (2, 118, "COLLINS ARRIVES", "Smaller than his waistcoat. Deeper in his bow. Already speaking."),
    (2, 119, "THE LADY CATHERINE RECITAL", "Eleven and a half minutes. A personal best. Lord B-B timed it."),
    (2, 120, "COLLINS ASSESSES THE DAUGHTERS", "He selected Eliza. Lady Catherine would probably approve."),
    (2, 121, "COLLINS SELECTS ELIZA", "He announced this in a hallway. Eliza was around the corner."),
    (2, 122, "THE TOUR OF THE HOUSE", "He complimented every room as a future Lady Catherine-adjacent property."),
    (2, 123, "THE PIANOFORTE OBSERVATION", "He called Mary's playing charming. She believed him. Consequences followed."),
    (2, 124, "COLLINS PROPOSES TO ELIZA", "He cited Lady Catherine six times before arriving at the actual question."),
    (2, 125, "ELIZA REFUSES", "She refused three times. He explained why she hadn't."),
    (2, 126, "LADY W-B IS INFORMED", "She staggers. She fans herself. She seizes the doorframe."),
    (2, 127, "LORD BISCUIT-BOTTOMS WEIGHS IN", "Ten seconds of parenting. More than most fathers manage in a decade."),
    (2, 128, "COLLINS REGROUPS", "One morning in the wilderness of rejection. One backup plan."),
    (2, 129, "COLLINS AND CHARLOTTE", "He proposed. She accepted before the sentence was complete."),
    (2, 130, "CHARLOTTE'S REASONING", "A comfortable home. A door she can close. That is enough."),
    (2, 131, "ELIZA'S HORROR", "Charlotte chose with eyes open and was content. This was worse."),
    (2, 132, "LADY W-B ON THE BETRAYAL", "Charlotte had stolen her clergyman. Not that she wanted the clergyman."),
    (2, 133, "LORD BISCUIT-BOTTOMS ON COLLINS AND CHARLOTTE", "The most rational catastrophe he had witnessed this quarter."),
    (2, 134, "THE ENGAGEMENT CELEBRATED", "Three courses, four toasts, five references to Lady Catherine."),
    (2, 135, "GASTON'S ASSESSMENT", "He is a garnish. She is sturdy bread. Together: adequate."),
    (2, 136, "MARY AND COLLINS: A MOMENT", "Two people who had never been listened to found each other."),
    (2, 137, "CHARLOTTE'S PLAN", "Every escape route identified. Every hour of solitude accounted for."),
    (2, 138, "THE WEDDING OF COLLINS AND CHARLOTTE", "He wept. She did not, having already processed this and moved on."),
    (2, 139, "ELIZA'S FAREWELL TO CHARLOTTE", "Two women who chose opposite paths. An honest kind of friendship."),
    (2, 140, "COLLINS DEPARTS LONGBOURN", "He bowed to the breakfast room. The library. The stairs."),
    (2, 141, "LADY W-B RECALIBRATES", "One daughter lost to pragmatism. The list grows longer."),
    (2, 142, "COLONEL FITZWILLIAM DEPARTS", "He accidentally revealed three things Darcy preferred locked in a vault."),
    (2, 143, "DARCY'S WITHDRAWAL", "A lighthouse attempting to be inconspicuous. The light keeps going."),
    (2, 144, "JANE'S LONDON PLAN", "She would visit family. It was not about the trip."),
    (2, 145, "THE DEPARTURE", "Jane left with quiet hope, clean gloves, and courage she did not know she had."),
    (2, 146, "JANE IN LONDON", "'I am quite well.' The Regency equivalent of a distress flare."),
    (2, 147, "THE CALL ON CAROLINE", "Caroline was warm for exactly ninety seconds. Devastating."),
    (2, 148, "CAROLINE'S REPLY", "A return call of fifteen minutes, standing up. A door closing while smiling."),
    (2, 149, "JANE'S LETTER", "Jane wrote that Caroline was 'kind.' Eliza translated fluently."),
    (2, 150, "BINGLEY DOES NOT CALL", "Two miles apart in London. His sister had decided the distance should remain."),
    (2, 151, "CAROLINE AND DARCY", "The decision was made over tea. Jane's future decided in her absence."),
    (2, 152, "BINGLEY IS MANAGED", "He believed his sister because he was too good not to. That is the tragedy."),
    (2, 153, "NETHERFIELD CLOSES", "The space where something was. Meryton felt the absence like a pulled tooth."),
    (2, 154, "JANE COMES HOME", "Neat, composed, golden. The right smile. Entirely empty."),
    (2, 155, "ELIZA'S FURY", "The quiet kind. The dangerous kind. The kind that remembers everything."),
    (2, 156, "LORD BISCUIT-BOTTOMS AND JANE", "Four words. The right four words."),
    (2, 157, "LADY W-B'S NEW TARGETS", "Bingley: closed. New volume: begun. Jane wears philosophical like a hat."),
    (2, 158, "ELIZA'S INVITATION", "An escape from everything. She accepted with unseemly haste."),
    (2, 159, "THE JOURNEY TO HUNSFORD", "Sir William talked for the entire journey. He said nothing of consequence."),
    (2, 160, "ARRIVAL AT THE PARSONAGE", "Charlotte showed her the parlour. Collins was rarely in it. By design."),
    (2, 161, "CHARLOTTE'S LIFE WITH COLLINS", "He addressed the vegetables. She read in peace. The system worked."),
    (2, 162, "ROSINGS SUMMONS", "Lady Catherine has UNDERLINED it. Collins trembles. Charlotte selects her dress."),
    (2, 163, "ROSINGS: THE DINNER", "She presided. Collins forgot to eat. Eliza studied the portraits."),
    (2, 164, "LADY CONSTANCE CRUMBLEWICK", "She spoke twice per dinner. Both sentences were the only things worth hearing."),
    (2, 165, "LADY CATHERINE INTERROGATES ELIZA", "Questions without anaesthetic, expecting the patient to be grateful."),
    (2, 166, "ELIZA DOES NOT FLINCH", "She answered every question without apology. Lady Catherine found this novel."),
    (2, 167, "DARCY ARRIVES AT ROSINGS", "He arrived. His step faltered one quarter of a second. She saw it."),
    (2, 168, "DARCY VISITS THE PARSONAGE", "Eleven words in forty-five minutes. Charlotte kept a tally."),
    (2, 169, "THE REPEAT VISITS", "Every day that week. Collins attributed this to Christian charity."),
    (2, 170, "FITZWILLIAM AND ELIZA", "He dropped a bomb casually. He walked on. He has no idea."),
    (2, 171, "ELIZA STOPS WALKING", "A reckoning was born in the gap between her stillness and his obliviousness."),
    (2, 172, "ELIZA GOES HOME ALONE", "New information. Old fury. Her opinion rebuilt from the foundations."),
    (2, 173, "THE HEADACHE", "A strategic headache. Charlotte knew. Charlotte said nothing."),
    (2, 174, "DARCY APPEARS", "He arrived, said almost nothing, and left an absence louder than his presence."),
    (2, 175, "ELIZA'S ASSESSMENT OF DARCY", "He was catastrophically, inarticately in love with her. Oh no."),
    (2, 176, "JANE'S LETTER", "Lydia invited to Brighton. The polka theme plays. Eliza closes her eyes."),
    (2, 177, "ELIZA'S ALARM", "A well-reasoned letter destined to be skimmed and overtaken by events."),
    (2, 178, "LORD BISCUIT-BOTTOMS'S POSITION", "He agreed with Eliza. He said so to no one. He returned to his newspaper."),
    (2, 179, "THE ROSINGS FAREWELL", "Lady Catherine paused at Eliza. An acknowledgement that she did not flinch."),
    (2, 180, "ELIZA HEADS HOME", "She knew more than when she left and was considerably less comfortable."),

    # ── SEASON 3: THE COLLAPSE ───────────────────────────────────────────────
    (3, 181, "DARCY FOLLOWS", "Rain. He has walked across his dignity to be here. He is trying."),
    (3, 182, "THE OPENING ATTEMPT", "Version three hundred and one. Worse than all the others."),
    (3, 183, "THE PROPOSAL, PART ONE", "He loves her. He has been fighting it. He reports this like a leak."),
    (3, 184, "THE PROPOSAL, PART TWO", "He is still listing the objections. He is still proposing. That is the problem."),
    (3, 185, "ELIZA'S REFUSAL", "The word was 'no.' She said it the way you read a sign to someone who keeps missing it."),
    (3, 186, "THE COUNTER-ARGUMENT", "Wickham. Bingley. Jane. The list is delivered without a smile."),
    (3, 187, "DARCY LEAVES", "He bowed. The bow was perfect. The perfection made it worse."),
    (3, 188, "ELIZA ALONE", "The proposal. Her refusal. The things said. Not crying. Thinking. Harder."),
    (3, 189, "THE LETTER ARRIVES", "Heavy paper. Black wax. She would wish she had not opened it. She would be glad she did."),
    (3, 190, "THE LETTER: WICKHAM", "The living was never refused. Wickham took three thousand pounds instead."),
    (3, 191, "THE LETTER: GEORGIANA", "Fifteen. Shy. Sweet. Wickham found her at Ramsgate. Darcy arrived in time."),
    (3, 192, "THE LETTER: BINGLEY AND JANE", "He admitted he may have been wrong. In fewer words than everything else."),
    (3, 193, "ELIZA READS IT TWICE", "Then a third time. The letter will be read more times than intended."),
    (3, 194, "THE REASSESSMENT BEGINS", "Every opinion. Both of them. Needs rebuilding. Spectacularly."),
    (3, 195, "ELIZA AND WICKHAM: RETROSPECTIVE", "He told a stranger his entire history at their first meeting. Who does that?"),
    (3, 196, "ELIZA AND DARCY: RETROSPECTIVE", "The visits. The silences. The returns. They look considerably different now."),
    (3, 197, "RETURNING HOME", "Everything rearranged inside her. She has told no one any of it."),
    (3, 198, "JANE MEETS HER", "Eliza tells her approximately none of what happened."),
    (3, 199, "LADY W-B'S NEWS", "Brighton! Officers! What could possibly go wrong? Several things."),
    (3, 200, "LORD BISCUIT-BOTTOMS OBSERVES", "He agrees from behind his paper, where agreement cannot be actioned."),
    (3, 201, "LYDIA PACKS FOR BRIGHTON", "Twice the clothing, zero judgment. The trunk will not close."),
    (3, 202, "KITTY'S DEVASTATION", "She is not invited to Brighton. She tells the hall mirror. Twice."),
    (3, 203, "WICKHAM IN BRIGHTON", "Charming the regiment. Charming the wives. Ruffington takes notes."),
    (3, 204, "LORD VELVETTHORN REAPPEARS", "Wickham's posture shifts by one degree when he sees him."),
    (3, 205, "ELIZA VISITS THE GARDINERS", "The summer plan: north. Derbyshire. Pemberley is five miles off."),
    (3, 206, "THE NORTHERN JOURNEY", "She is thinking about one thing specifically. The hills disagree."),
    (3, 207, "THE DECISION", "The family is not expected until tomorrow. She fixes her bonnet."),
    (3, 208, "APPROACHING PEMBERLEY", "Below: Pemberley. The orchestra swells. The mouth opens. The ache begins."),
    (3, 209, "THE HOUSEKEEPER'S ACCOUNT", "He was the sweetest-tempered boy. He has never spoken a cross word."),
    (3, 210, "ELIZA'S FACE", "Standing before the portrait. A softening. A reckoning. The portrait knows."),
    (3, 211, "HE IS NOT SUPPOSED TO BE HERE", "A day early. They collide on the path. The chambermaid feels terrible."),
    (3, 212, "THE FIRST LOOK", "A duck passes between them without reading the room."),
    (3, 213, "THE RECOVERY", "He was actually warm. Not performing. She had not prepared for this."),
    (3, 214, "THE CHANGED MAN", "He greeted the Gardiners with zero condescension. She noticed everything."),
    (3, 215, "LORD VELVETTHORN WATCHES", "From the hill, a satisfied nod, like a chess piece moving into position."),
    (3, 216, "GEORGIANA", "Shy, sweet, terrified. Then a whispered hello. Then a small smile. Undone."),
    (3, 217, "CAROLINE APPEARS", "The pause before 'surprise' contained the word 'disappointment' in full."),
    (3, 218, "CAROLINE'S ASSESSMENT", "He is smiling. At a dog. The campaign enters its final phase."),
    (3, 219, "BINGLEY APPEARS", "He asked after Jane immediately. Subtlety is a skill Bingley decided against."),
    (3, 220, "ELIZA WATCHES BINGLEY", "A man whose confidence was removed. She knows now who removed it."),
    (3, 221, "DARCY AND ELIZA: THE WALK", "The conversation was easier. Two people agreeing about shrubbery."),
    (3, 222, "THE ALMOST-ACKNOWLEDGMENT", "He almost spoke. She almost spoke. The weather received their full attention."),
    (3, 223, "GEORGIANA AND ELIZA", "Darcy watched Eliza be gentle with the person he loves most. Undone."),
    (3, 224, "CAROLINE'S ATTACK", "A remark about Wickham. Sharp. Calibrated. Received with calm that cuts glass."),
    (3, 225, "DARCY INTERCEPTS", "One word to Caroline. 'Don't.' One eyebrow. She retreated."),
    (3, 226, "THE PEMBERLEY LIBRARY", "Floor to ceiling. Thousands of volumes. She forgot everything else for eight seconds."),
    (3, 227, "THE LIBRARY CONVERSATION", "Finishing each other's quotations. The hinge. The whole story turns here."),
    (3, 228, "LORD VELVETTHORN INTRODUCES HIMSELF", "He owed Darcy considerably. He has come to say so. He leaves."),
    (3, 229, "VELVETTHORN'S HISTORY", "He saved the estate. He told no one. He considers kindness a private matter."),
    (3, 230, "BINGLEY AND DARCY", "A closed door. Two shadows. When it opened, Bingley's tail had resumed."),
    (3, 231, "THE DINNER AT PEMBERLEY", "Gaston borrowed for the evening. Everyone except Gaston will regret this."),
    (3, 232, "GASTON ON THE TABLE", "More wine for the gentleman who cannot stop looking at the lady."),
    (3, 233, "CAROLINE'S FINAL ATTEMPT", "She performed maximum elegance. His head turned when Eliza laughed."),
    (3, 234, "THE EVENING ENDS", "He helped her into the carriage. The contact lasted one second too long."),
    (3, 235, "THE GOODBYE", "He stood there after it disappeared. He stood there a while longer."),
    (3, 236, "IN THE CARRIAGE", "She looked out the window. Aunt Gardiner placed a paw on hers."),
    (3, 237, "THE LETTER", "A letter arrives. She goes cold. The cup stops halfway to her mouth."),
    (3, 238, "JANE'S LETTER", "Lydia is missing. She has gone with Wickham. Not to a church."),
    (3, 239, "ELIZA'S FACE", "She understood three things simultaneously. The pattern. The culpability."),
    (3, 240, "ELIZA TELLS DARCY", "I will deal with this. Five words. Already moving. Not a promise. A fact."),
    (3, 241, "THE RACE HOME", "The carriage cannot go fast enough. The road remains exactly as long."),
    (3, 242, "LONGBOURN IN CRISIS", "Lady W-B is horizontal and has been since the note arrived."),
    (3, 243, "LORD BISCUIT-BOTTOMS STANDS", "The newspaper is on the desk. This alone tells Eliza everything."),
    (3, 244, "THE NOTE", "Three exclamation marks and zero evidence of thought."),
    (3, 245, "UNCLE GARDINER TO LONDON", "He goes. Steady. Capable. The only one currently above crisis speed."),
    (3, 246, "JANE AND ELIZA", "Sitting together the way they did when the world was smaller and less capable of harm."),
    (3, 247, "LADY W-B'S CONDITION", "Day four. She has not moved except for tea and dramatic cushion rearrangements."),
    (3, 248, "WICKHAM'S DEBTS", "He owes everyone. A bookseller's debt was the only one that surprised anyone."),
    (3, 249, "THE PRICE", "The figure. Too large. Lord Biscuit-Bottoms looks old for the first time."),
    (3, 250, "UNCLE GARDINER'S LETTER", "It is arranged. He is vague about the source. Eliza detects evasion at two hundred miles."),
    (3, 251, "WHO PAID", "She writes to Uncle Gardiner. She is becoming certain. The certainty is complicated."),
    (3, 252, "DARCY'S ABSENCE", "He has not written. He is doing something so large it requires anonymity."),
    (3, 253, "SERGEANT RUFFINGTON KNOWS", "A tuxedo cat in London, arguing, paying, settling debts not his own."),
    (3, 254, "LYDIA AND WICKHAM: MARRIED", "Technically a wedding. The word technically is doing enormous work here."),
    (3, 255, "LYDIA RETURNS", "'Lord! How jealous you must all be!' The house is not unchanged."),
    (3, 256, "LYDIA'S ACCOUNT", "A tuxedo cat helped. She says this casually. Eliza's cup freezes."),
    (3, 257, "ELIZA'S EXPRESSION", "He stood up at the wedding of the woman who refused him. For her family."),
    (3, 258, "WICKHAM ARRIVES", "His smile is ten percent too wide. He cannot hold Eliza's gaze."),
    (3, 259, "ELIZA AND WICKHAM", "She is finished with him. Clear-eyed. Not angry. Simply done."),
    (3, 260, "LORD BISCUIT-BOTTOMS ON WICKHAM", "The sort of gentleman who steals the silver and helps you look for it."),
    (3, 261, "THE SETTLEMENT", "They depart north. Lydia waves. Lord B-B exhales for the first time in weeks."),
    (3, 262, "AFTER", "Eliza stands at the window, thinking about a man who paid for her sister's wedding."),
    (3, 263, "ELIZA WRITES TO AUNT GARDINER", "Please tell me it was Darcy. The 'please' is where the story turns."),
    (3, 264, "LORD VELVETTHORN'S LAST APPEARANCE", "One tip of the hat to Eliza. No one else. The road closes behind him."),
    (3, 265, "LADY W-B RECOVERS", "She is off the sofa. She has a new list. She mentions Bingley's name."),
    (3, 266, "JANE'S HOPE", "She says nothing about Bingley. But the page has not turned in twenty minutes."),
    (3, 267, "DARCY AND HIS DECISION", "He is past analysis. He is in the place where decision lives."),
    (3, 268, "CAROLINE'S INTELLIGENCE", "She mentioned Bingley spoke of Meryton fondly. She had lost the argument."),
    (3, 269, "HORTENSIA BROADCASTS", "Something is coming. She does not know what. This has never slowed her down."),
    (3, 270, "THE END OF SEASON THREE", "North, a light goes out. A carriage is made ready."),

    # ── SEASON 4: THE RECKONING ──────────────────────────────────────────────
    (4, 271, "AUNT GARDINER WRITES BACK", "Information one has suspected but hoped might be someone else's problem."),
    (4, 272, "THE CONFIRMATION", "Darcy found them. Darcy paid. Darcy told no one. She sets the letter down."),
    (4, 273, "ELIZA SITS DOWN", "Some truths require furniture."),
    (4, 274, "THE REASSESSMENT, COMPLETE", "A case built with the thoroughness of a barrister. The accuracy of a weather vane."),
    (4, 275, "ELIZA AND JANE", "She told Jane everything. Jane kept saying 'no' in escalating disbelief."),
    (4, 276, "JANE'S QUESTION", "Do you love him? A pause so loud it could be heard in the next county."),
    (4, 277, "WHAT ELIZA FEELS", "Large, inconvenient, installed without permission, like a piano in a hallway."),
    (4, 278, "BISCUIT-BOTTOMS NOTICES", "He was saying nothing about Darcy with such precision it was a full conversation."),
    (4, 279, "LADY W-B'S CONTINUED SCHEMES", "The list is colour-coded. Lord Biscuit-Bottoms retreats."),
    (4, 280, "LORD BISCUIT-BOTTOMS ON THE LIST", "The colour-coding suggests emotional escalation. He is not wrong."),
    (4, 281, "CAROLINE'S LATEST", "Bingley bounds past her toward Longbourn. Her smile is architectural."),
    (4, 282, "BINGLEY IS BACK", "Netherfield lit up. Meryton noticed in an hour. Hortensia in a minute."),
    (4, 283, "BINGLEY CALLS AT LONGBOURN", "They were both in the same room. Eliza stepped on Lady W-B's paw."),
    (4, 284, "THE RECOVERY", "They spoke over each other and laughed. The oldest method of beginning again."),
    (4, 285, "DARCY WITH BINGLEY", "He enters Longbourn behind Bingley. The room remembers his last visit."),
    (4, 286, "THE PARALLEL VISITS", "Left: laughter. Right: silence. Both rooms contained the same emotion."),
    (4, 287, "LADY W-B ON BINGLEY", "SECURED. In capitals. She turns to the Eliza column and narrows her eyes."),
    (4, 288, "CAROLINE'S STRATEGIC WITHDRAWAL", "The battle is over. She is focused entirely on choosing the correct exit."),
    (4, 289, "DARCY'S DIFFICULTY", "He cannot un-propose. He can only try differently. No manual exists for this."),
    (4, 290, "ELIZA'S DIFFICULTY", "One does not un-refuse. There is no card for it. No accepted phrase."),
    (4, 291, "THE AWKWARD WALK", "They ended up side by side. Everyone pretended not to notice."),
    (4, 292, "CONVERSATION ON THE WALK", "She thanked him. He said nothing. The silence was the information."),
    (4, 293, "ZELDA'S SECOND READING", "You are almost finished being afraid. One card. A gate, half open."),
    (4, 294, "BINGLEY PREPARES", "He asked for advice. Darcy said one word. Bingley waited for more."),
    (4, 295, "COLONEL FITZWILLIAM REAPPEARS", "He has news and is sharing it with the most operationally catastrophic person available."),
    (4, 296, "FITZWILLIAM'S ACCIDENTAL BROADCAST", "Darcy speaks warmly of your second daughter. This was operationally catastrophic."),
    (4, 297, "LADY W-B ON DARCY", "DARCY. In red ink. Underlined twice. Added to the list."),
    (4, 298, "LORD BISCUIT-BOTTOMS LOWERS THE PAPER", "You would not have been happy with anyone less than your equal."),
    (4, 299, "JANE AND BINGLEY IN THE GARDEN", "Lady W-B at the window, nose pressed to the glass, fogging the pane."),
    (4, 300, "THE PROPOSAL: BINGLEY TO JANE", "Bingley dropped to one knee. Lady W-B's face: unguarded, unstrategic joy."),
    (4, 301, "JANE COMES INSIDE", "Silence. The kind that comes before weather."),
    (4, 302, "THE ANNOUNCEMENT", "Lady W-B made a sound between a Pomeranian yip and a cathedral organ."),
    (4, 303, "LORD BISCUIT-BOTTOMS'S RESPONSE", "He said it quietly. He retreated behind the newspaper. His eyes were bright."),
    (4, 304, "ELIZA AND JANE", "Too much to say. Not enough words. She squeezed her paws instead."),
    (4, 305, "LADY W-B'S VICTORY LAP", "Every household in the county within forty-eight hours. Hortensia was scooped."),
    (4, 306, "CAROLINE'S CONGRATULATIONS", "Every word correct. The tone correct. Nothing felt. Jane believed her anyway."),
    (4, 307, "BINGLEY AND DARCY", "Bingley glowing. Darcy watching. Your turn, old friend."),
    (4, 308, "MRS WOOFSLEY'S OPINION", "Nine Pugs in celebratory ribbons. She had predicted this. In May."),
    (4, 309, "GASTON'S ENGAGEMENT DINNER", "The consomme for joy. The souffle for hope. The dessert for the not-yet-brave."),
    (4, 310, "DARCY AT THE ENGAGEMENT DINNER", "Their eyes met. A candle guttered. Someone coughed. They looked away."),
    (4, 311, "ELIZA'S WALK", "She walked. He rode. They met on the road. The road was not surprised."),
    (4, 312, "THE ROAD CONVERSATION", "He began something and did not finish. It was going to be the right sentence."),
    (4, 313, "COLONEL FITZWILLIAM AND THE TRUTH", "He has wanted to see you since Easter. Lovely morning! He walked on."),
    (4, 314, "ELIZA PROCESSES", "'He has wanted to see you since Easter' is not a sentence one walks away from quickly."),
    (4, 315, "LADY W-B'S NEW LIST", "ELIZA. DARCY. Arrow connecting them. She shows no one. She closes the desk."),
    (4, 316, "THE HUFFINGTON-SCRATCH REACTION", "Lady Moppet mentions accomplished daughters. Lady W-B offers the last biscuit."),
    (4, 317, "SIR REGINALD AND BISCUIT-BOTTOMS", "Port. Silence. A nod returned. The most satisfying conversation of the period."),
    (4, 318, "BINGLEY AND JANE: PLANNING", "Lady W-B has forty-seven thoughts on the seating."),
    (4, 319, "MARY'S PERSPECTIVE", "A philosophical observation on matrimony that was, against all precedent, correct."),
    (4, 320, "KITTY'S RECOVERY", "Alone without Lydia for the first time, she discovered she had a nose of her own."),
    (4, 321, "KITTY ALONE", "She said something thoughtful. Eliza looked at her as if seeing her clearly."),
    (4, 322, "AUNT GARDINER'S RETURN", "I suspected you needed to know. One sentence. It was enough."),
    (4, 323, "DARCY AND THE DECISION", "He has eliminated every insult from the first proposal. Much shorter now."),
    (4, 324, "THE REHEARSAL", "He rehearsed at Pemberley. The portraits watched. They were not helpful."),
    (4, 325, "CAROLINE'S RETREAT", "You will be happy here. I will be happy elsewhere. She meant every word."),
    (4, 326, "THE FAREWELL TO CAROLINE", "Something genuine flickered behind the architecture. One fractional moment."),
    (4, 327, "THE MR HURST MYSTERY", "He has been asleep in a chair all season. He will not be disturbed."),
    (4, 328, "HORTENSIA'S LATEST", "Something is approaching in the direction of Longbourn. She is professional."),
    (4, 329, "LADY W-B'S PREMONITION", "I can feel it. How do you know? He turns a page."),
    (4, 330, "THE CALM BEFORE", "The gate is empty. It will not be empty for long."),
    (4, 331, "THE CARRIAGE AT LONGBOURN", "THE carriage. The crest. The trees lean away. The organ swells."),
    (4, 332, "LADY CATHERINE ARRIVES", "She entered Longbourn without waiting. She has never encountered an applicable boundary."),
    (4, 333, "THE SURVEY", "The parlour: insufficient. The furniture: beneath comment. Commented upon."),
    (4, 334, "LADY W-B'S REACTION", "The honour immense. The hostility also immense. She offered tea."),
    (4, 335, "LADY CONSTANCE IN THE CARRIAGE", "She did not come inside. She watches the house. She has chosen the better seat."),
    (4, 336, "THE WALK IN THE GARDEN", "Lady Catherine set the tempo. Eliza's stride matched her step for step."),
    (4, 337, "LADY CATHERINE'S DEMAND", "She demands denial the way gravity requires downward."),
    (4, 338, "ELIZA'S RESPONSE", "I am not engaged to Mr Darcy. Factually true. The emphasis did considerable work."),
    (4, 339, "THE PAUSE", "Close on Eliza's face. One second. Two. Lady Catherine noted the pause."),
    (4, 340, "ELIZA REFUSES TO PROMISE", "I will make no promise of the kind. Her gaze held steady. No apology."),
    (4, 341, "LADY CATHERINE'S POSITION", "Magnificent. Completely wrong. Magnificently, completely wrong."),
    (4, 342, "ELIZA ON THE ARRANGEMENT", "If the arrangement is certain, why has Darcy not spoken to Miss de Paw?"),
    (4, 343, "LADY CATHERINE ESCALATES", "Birth. Fortune. The elopement. Each word precise, each word intended to wound."),
    (4, 344, "ELIZA'S FINAL WORD", "You have said everything. Nothing will be changed. I thank you for the visit."),
    (4, 345, "LADY CATHERINE DEPARTS", "Lady Constance looked back at the house once. No one saw. The road closed."),
    (4, 346, "LADY W-B'S DEBRIEF", "Eliza told her nothing. Lady W-B invented the rest. More dramatic."),
    (4, 347, "LORD BISCUIT-BOTTOMS'S ASSESSMENT", "Lady Catherine coming here means Darcy is thinking about coming here."),
    (4, 348, "LADY CATHERINE AND DARCY", "She reported the refusal. She expected alliance. She received neither."),
    (4, 349, "DARCY HEARS THE REPORT", "She refused to promise. His whiskers twitched once. Everything behind his eyes shifted."),
    (4, 350, "DARCY'S CONCLUSION", "Not a no. In fact, the opposite of a no. The best non-answer he had ever received."),
    (4, 351, "THE PLAN", "No list. No analysis. A question and a heartbeat and a carriage."),
    (4, 352, "ZELDA'S FINAL READING", "All the cards. She looked at them. She said yes. Just that."),
    (4, 353, "HORTENSIA'S INTELLIGENCE", "A tuxedo cat. On the Longbourn road. VERY good carriage."),
    (4, 354, "THE NEIGHBOURHOOD WATCHES", "Private moments become public theatre. Love arrives with an audience."),
    (4, 355, "JANE TO ELIZA", "I think he is coming. I know. Her bonnet was crooked. She left it."),
    (4, 356, "MRS WOOFSLEY'S INTRUSION", "Six Pugs and a question. Redirected with force and perfect timing."),
    (4, 357, "PROFESSOR BARKSWORTH", "Mary hit a wrong note, then a right one, then a beautiful one."),
    (4, 358, "LORD BISCUIT-BOTTOMS PREPARES", "He folded the newspaper. He stood up. Longbourn held its breath."),
    (4, 359, "THE GATE", "The carriage. The lane. The gate. The crooked bonnet in the doorway."),
    (4, 360, "HE IS AT THE GATE", "He walked through. She did not move. The distance closed. One note. Black."),

    # ── SEASON 5: THE RESOLUTION ─────────────────────────────────────────────
    (5, 361, "DARCY ENTERS", "He is patient. He is wearing the coat. Lady W-B has rattled the china cabinet."),
    (5, 362, "THE EXCUSE", "He asked for the garden. Lady W-B said yes before Eliza opened her mouth."),
    (5, 363, "THE GARDEN", "The same bench. The same roses. A very different cat."),
    (5, 364, "HE BEGINS", "He brought only the question. No speech prepared."),
    (5, 365, "NO REHEARSED LIST", "No conditions. No qualifications. Just a cat, in a garden, asking."),
    (5, 366, "ELIZA'S ANSWER", "They are not hopeless. Quietly. Completely."),
    (5, 367, "THE MOMENT", "He took her hand. She let him. The Love Theme played its full statement."),
    (5, 368, "WHAT HE SAYS", "I love you. More than before. His tail moved. Once. To the left."),
    (5, 369, "WHAT SHE SAYS", "Grateful for the letter since the day she received it. She smiles."),
    (5, 370, "THE NARRATOR", "It only took three hundred and seventy episodes. Genuinely pleased."),
    (5, 371, "BACK INSIDE", "Lord Biscuit-Bottoms noted the expression. He raised the newspaper fractionally higher."),
    (5, 372, "DARCY TO LORD BISCUIT-BOTTOMS", "He voluntarily set down the newspaper. Longbourn held its breath."),
    (5, 373, "THE CONVERSATION", "We did not hear it. His face said: you will do."),
    (5, 374, "LADY W-B IS NOT TOLD YET", "She will need a chair. And a strong cup of tea. Perhaps two chairs."),
    (5, 375, "THE ANNOUNCEMENT", "Mama. Mr Darcy has asked me to marry him. I have said yes."),
    (5, 376, "LADY W-B'S RESPONSE", "MR DARCY! TEN THOUSAND A YEAR! The finest man in England!"),
    (5, 377, "JANE IS TOLD", "Jane cried immediately. Eliza cried. I am not crying. I am narrating."),
    (5, 378, "DARCY AND ELIZA: THE EVENING", "Mary played something terrible. Nobody asked her to stop. This is happiness."),
    (5, 379, "LORD BISCUIT-BOTTOMS'S ONE-LINER", "Longbourn has never been so full of joy. This explains the volume."),
    (5, 380, "THE ENGAGEMENT", "Two cats, two Fetchworth daughters. The county will not recover for years."),
    (5, 381, "LADY W-B BROADCASTS", "Every household in Hertfordshire. Ninety seconds per stop. No prisoners."),
    (5, 382, "HORTENSIA'S RESPONSE", "I know. Since yesterday. Congratulations. The tea is Darjeeling."),
    (5, 383, "THE HUFFINGTON-SCRATCHES REACT", "Lady Moppet arrived with biscuits and a strategy to revise."),
    (5, 384, "MRS WOOFSLEY'S CELEBRATION", "An uninvited party. Pink and blue ribbons on all nine Pugs. Laminated seating plan."),
    (5, 385, "LADY CATHERINE'S FURY", "Her whiskers extended to full horizontal. Lady Constance said: it's done."),
    (5, 386, "LADY CONSTANCE ON THE MATTER", "You cannot stop water. Lady Catherine found this insufficient. It was not."),
    (5, 387, "DARCY WRITES TO LADY CATHERINE", "Four sentences. No apology. No explanation. No request for approval."),
    (5, 388, "LADY CATHERINE'S EVENTUAL REPLY", "Three weeks later. Very short. Very correct. Lady Constance drafted it."),
    (5, 389, "CAROLINE'S LETTER", "To Eliza: I find, to my surprise, that I mean it. Grace."),
    (5, 390, "BINGLEY ON DARCY'S ENGAGEMENT", "I KNEW it! Episode two forty-one, you asked if I disliked her. I FELT it."),
    (5, 391, "GEORGIANA AND ELIZA", "She called her sister. She had been waiting to write that word since Pemberley."),
    (5, 392, "COLONEL FITZWILLIAM", "He announced he had introduced them. He was wrong and broadly correct."),
    (5, 393, "WICKHAM HEARS", "Well done, Darcy. The smile was his most complicated to date."),
    (5, 394, "LYDIA'S REACTION", "Well done! I did not think you had it in you! This is high praise from Lydia."),
    (5, 395, "MARY'S PHILOSOPHICAL OBSERVATION", "Happiness, when deserved, arrives not as reward but as recognition."),
    (5, 396, "KITTY'S MOMENT", "Was there someone I missed, while I was following Lydia into everything?"),
    (5, 397, "AUNT GARDINER'S SATISFACTION", "She read both letters and sat, very still, with deep quiet satisfaction."),
    (5, 398, "THE WEDDING PLANS", "Two weddings. Same day. Same church. Reverend Tailwagger has been there since dawn."),
    (5, 399, "GASTON IS COMMISSIONED", "Complete latitude. His eyes widened. He began immediately. With the cake."),
    (5, 400, "LONGBOURN THE NIGHT BEFORE", "Lord B-B read his paper. He did not turn the page. He was holding on."),
    (5, 401, "THE MORNING", "A mother who appeared to have conquered the laws of physics."),
    (5, 402, "THE DRESSES", "Jane in gold. Eliza in something unexpected and perfect. Lady W-B in architecture."),
    (5, 403, "LORD BISCUIT-BOTTOMS GETS READY", "The wig slid. He left it. A father ready to give away two daughters."),
    (5, 404, "THE CARRIAGES", "Lady W-B had a system, a list, and hand signals. No repeats of Netherfield."),
    (5, 405, "THE REVEREND TAILWAGGER", "His remarks, backup remarks, and backup backup remarks for when he cries."),
    (5, 406, "MRS WOOFSLEY ARRIVES", "Uninvited, nine Pugs in wedding white, laminated seating plan. She accommodates herself."),
    (5, 407, "GENERAL SLOBBERCHOPS", "Wrong church, wrong village, wrong day. Still arrived with twelve minutes to spare."),
    (5, 408, "THE CHURCH FILLS", "Every bonnet in Hertfordshire present. Charlotte Collins smiles warmly."),
    (5, 409, "THE GROOMS ARRIVE", "Bingley's tail rippled the wedding coat. Darcy's left ear twitched."),
    (5, 410, "THE BRIDES ENTER", "The crooked bonnet. He saw it. Everything held let go."),
    (5, 411, "THE CEREMONY: BINGLEY AND JANE", "He said the vows as if he had been waiting since the first assembly. He had."),
    (5, 412, "THE CEREMONY: DARCY AND ELIZA", "They said the words. They meant them. For once, nothing to add."),
    (5, 413, "LORD BISCUIT-BOTTOMS", "His expression was his own. I will not describe it. Some things are not for narrators."),
    (5, 414, "LADY W-B TRANSCENDS", "Crying from the first vow to the last. Bonnet migrated. She was magnificent."),
    (5, 415, "THE WEDDING BREAKFAST", "Gaston wept. Not from sadness. From the beauty of what he had accomplished."),
    (5, 416, "THE CAKE", "Three tiers. Sugar flowers. Tiny edible portraits of both couples. Masterpiece."),
    (5, 417, "THE CAKE SITUATION", "The cause remains disputed. The result was unanimous."),
    (5, 418, "THE AFTERMATH", "Lady W-B stood in the cake remains. The county waited for her verdict."),
    (5, 419, "LORD BISCUIT-BOTTOMS", "Completely clean. Not a mark. He handed her a napkin without looking up."),
    (5, 420, "THE CARRIAGES DEPART", "The crooked bonnet. The tuxedo cat. Four hundred and twenty episodes. She stepped in."),
]

def make_tiktok_instagram_text(ep_num, title, logline):
    return f"EP.{ep_num:03d} | {title}\n\n{logline}\n\n{HASHTAGS_SOCIAL}"

def make_youtube_text(ep_num, title, logline, season_num):
    season_name = SEASON_NAMES[season_num]
    return (
        f"EP.{ep_num:03d} | {title}\n\n"
        f"{logline}\n\n"
        f"Paws & Prejudice — {season_name}\n"
        f"New episode every day.\n\n"
        f"{HASHTAGS_YOUTUBE}"
    )

def get_due_date(ep_num):
    """
    5 episodes per day starting 2026-03-30T18:00:00+01:00
    EP 1-5 → day 0, EP 6-10 → day 1, etc.
    """
    day_offset = (ep_num - 1) // 5
    base = datetime(2026, 3, 30, 18, 0, 0, tzinfo=timezone(timedelta(hours=1)))
    dt = base + timedelta(days=day_offset)
    return dt.isoformat()

def create_buffer_idea(title, text):
    """Create a Buffer Idea (text-only draft) in the Ideas section."""
    mutation = """
    mutation CreateIdea($input: CreateIdeaInput!) {
      createIdea(input: $input) {
        ... on Idea {
          id
        }
        ... on IdeaResponse {
          idea {
            id
          }
        }
        ... on InvalidInputError {
          message
        }
        ... on UnauthorizedError {
          message
        }
        ... on UnexpectedError {
          message
        }
        ... on LimitReachedError {
          message
        }
      }
    }
    """
    variables = {
        "input": {
            "organizationId": ORG_ID,
            "content": {
                "title": title,
                "text": text,
            }
        }
    }
    payload = {"query": mutation, "variables": variables}
    resp = requests.post(GRAPHQL_URL, headers=HEADERS, json=payload, timeout=30)
    return resp.status_code, resp.json()

def is_success(resp):
    """Check if createIdea response is a success. Returns (ok, idea_id_or_error_msg)."""
    data = resp.get("data", {})
    if not data:
        return False, None
    create_idea = data.get("createIdea", {})
    if not create_idea:
        return False, None
    # Direct Idea object
    if create_idea.get("id"):
        return True, create_idea["id"]
    # IdeaResponse wrapper
    idea = create_idea.get("idea")
    if idea and idea.get("id"):
        return True, idea["id"]
    # Error
    msg = create_idea.get("message", "Unknown error")
    return False, msg

def test_api():
    """Test with EP.001 TikTok/Instagram idea before running everything."""
    print("=== TEST API CALL (createIdea) ===")
    ep = EPISODES[0]
    season_num, ep_num, title, logline = ep
    text = make_tiktok_instagram_text(ep_num, title, logline)
    idea_title = f"[TikTok+IG] EP.{ep_num:03d} | {title}"
    print(f"Idea title: {idea_title}")
    print(f"Text preview: {text[:80]}...")
    status, resp = create_buffer_idea(idea_title, text)
    print(f"HTTP Status: {status}")
    print(f"Response: {json.dumps(resp, indent=2)}")
    ok, idea_id_or_msg = is_success(resp)
    if status == 200 and ok:
        print(f"SUCCESS! Idea ID: {idea_id_or_msg}")
        return True
    else:
        print(f"FAILED: {idea_id_or_msg}")
        return False

def load_completed(log_path):
    """Load set of already-completed (EP_num, platform) pairs from log."""
    completed = set()
    if os.path.exists(log_path):
        with open(log_path, "r") as f:
            for line in f:
                if line.startswith("OK "):
                    parts = line.strip().split()
                    if len(parts) >= 3:
                        ep_part = parts[1]   # e.g. EP.003
                        platform = parts[2]   # e.g. TikTok+IG
                        try:
                            ep_num = int(ep_part.split(".")[1])
                            completed.add((ep_num, platform))
                        except Exception:
                            pass
    return completed

def run_all():
    """
    Create Buffer Ideas for all 420 episodes.
    2 ideas per episode: one for TikTok+Instagram copy, one for YouTube copy.
    840 API calls total. Supports resume from previous partial run.
    """
    log_path = "/Users/davidsheldrick/Desktop/paws_and_prejudice/buffer_results.log"

    # Load previously completed items to support resume
    completed = load_completed(log_path)
    if completed:
        print(f"Resuming: {len(completed)} ideas already created, skipping those.\n")

    total_success = len(completed)  # count existing successes
    total_fail = 0
    errors = []

    # 2 ideas per episode (TikTok/IG combined + YouTube)
    total_calls = len(EPISODES) * 2
    call_count = 0

    print(f"\n=== STARTING FULL RUN: {total_calls} createIdea calls ===\n")
    print("NOTE: Using createIdea (text-only drafts) — media can be added in Buffer UI.\n")

    with open(log_path, "a") as logf:
        logf.write(f"\n--- Run started: {datetime.now().isoformat()} ---\n")

        for ep in EPISODES:
            season_num, ep_num, title, logline = ep
            due_at = get_due_date(ep_num)

            ti_text = make_tiktok_instagram_text(ep_num, title, logline)
            yt_text = make_youtube_text(ep_num, title, logline, season_num)

            ideas = [
                (f"[TikTok+IG] EP.{ep_num:03d} | {title}  [due:{due_at[:10]}]", ti_text, "TikTok+IG"),
                (f"[YouTube]   EP.{ep_num:03d} | {title}  [due:{due_at[:10]}]", yt_text, "YouTube"),
            ]

            for idea_title, text, platform in ideas:
                call_count += 1
                # Skip if already created in a previous run
                if (ep_num, platform) in completed:
                    continue
                retries = 0
                max_retries = 10
                while retries <= max_retries:
                    try:
                        status, resp = create_buffer_idea(idea_title, text)

                        # Handle 429 responses — could be per-minute rate limit OR daily quota
                        if status == 429:
                            errs = resp.get("errors", [])
                            ext = errs[0].get("extensions", {}) if errs else {}
                            code = ext.get("code", "")

                            if code == "QUOTA_EXCEEDED":
                                # Daily quota: wait until resetAt timestamp
                                reset_at_str = ext.get("resetAt")
                                if reset_at_str:
                                    reset_dt = datetime.fromisoformat(reset_at_str.replace("Z", "+00:00"))
                                    now_dt = datetime.now(timezone.utc)
                                    wait_secs = max(120, (reset_dt - now_dt).total_seconds() + 120)
                                else:
                                    wait_secs = 6 * 3600
                                print(f"\nDAILY QUOTA EXCEEDED. Waiting {wait_secs:.0f}s ({wait_secs/3600:.1f}h)...")
                                logf.write(f"QUOTA_EXCEEDED EP.{ep_num:03d} {platform:12s} waiting {wait_secs:.0f}s\n")
                                logf.flush()
                                time.sleep(wait_secs)
                            else:
                                # Per-minute rate limit
                                retry_after = int(ext.get("retryAfter", 900)) + 10
                                print(f"\nRATE LIMITED. Waiting {retry_after}s (EP.{ep_num:03d} {platform})...")
                                logf.write(f"RATE_LIMIT EP.{ep_num:03d} {platform:12s} waiting {retry_after}s\n")
                                logf.flush()
                                time.sleep(retry_after)

                            retries += 1
                            continue

                        ok, idea_id_or_msg = is_success(resp)
                        if status == 200 and ok:
                            total_success += 1
                            msg = f"OK  EP.{ep_num:03d} {platform:12s} {idea_id_or_msg}"
                        else:
                            total_fail += 1
                            err_msg = str(idea_id_or_msg)[:200] if idea_id_or_msg else json.dumps(resp)[:200]
                            errors.append(f"EP.{ep_num:03d} {platform}: HTTP {status} - {err_msg}")
                            msg = f"ERR EP.{ep_num:03d} {platform:12s} HTTP={status} {err_msg}"
                        break
                    except Exception as e:
                        total_fail += 1
                        errors.append(f"EP.{ep_num:03d} {platform}: Exception {str(e)}")
                        msg = f"EXC EP.{ep_num:03d} {platform:12s} {str(e)}"
                        break
                else:
                    total_fail += 1
                    msg = f"MAX_RETRY EP.{ep_num:03d} {platform:12s}"
                    errors.append(msg)

                logf.write(msg + "\n")
                logf.flush()

                if call_count % 50 == 0:
                    print(f"Progress: {call_count}/{total_calls} | Success: {total_success} | Fail: {total_fail}")

                # Small delay to be respectful of rate limits
                time.sleep(1.0)

        # Remove duplicate test idea (EP.001 was already created in test_api)
        summary = (
            f"\n=== SUMMARY ===\n"
            f"Total calls: {call_count}\n"
            f"Successes: {total_success}\n"
            f"Failures: {total_fail}\n"
            f"Finished: {datetime.now().isoformat()}\n"
        )
        logf.write(summary)
        if errors:
            logf.write("\n=== ERRORS ===\n")
            for e in errors:
                logf.write(e + "\n")

    print(summary)
    if errors:
        print(f"\nFirst 10 errors:")
        for e in errors[:10]:
            print(f"  {e}")

    return total_success, total_fail, errors

if __name__ == "__main__":
    log_path = "/Users/davidsheldrick/Desktop/paws_and_prejudice/buffer_results.log"

    # Check if we have existing completions — if so skip test and go straight to resume
    existing = load_completed(log_path)
    if existing:
        print(f"Found {len(existing)} existing ideas. Skipping test call — going straight to resume.\n")
    else:
        # Step 1: Test with one call
        ok = test_api()
        if not ok:
            print("\nTest call failed. Check rate limits or API key. Aborting.")
            sys.exit(1)
        print("\nTest call succeeded. Starting full run in 3 seconds...")
        time.sleep(3)

    # Step 2: Run all 840 createIdea calls (with resume)
    success, fail, errors = run_all()

    print(f"\nDone. {success} ideas created total, {fail} failures this run.")
    print("Results log: /Users/davidsheldrick/Desktop/paws_and_prejudice/buffer_results.log")
