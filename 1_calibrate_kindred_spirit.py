#!/usr/bin/env python3
"""
Kindred Spirit Calibration - Interactive CLI

A therapeutic exploration to discover your actual values through:
1. Contemporary political dilemmas (Phase 1 - 15 questions)
2. Timeless ethical questions (Phase 2 - 22 questions)
3. Personal/existential priorities (Phase 3 - 2+ questions)
4. Resonant figures - heroes with human flaws (Phase 4 - 20 figures)
5. Ethical frameworks (Phase 5 - 16 frameworks)

Total: ~75 questions. Progress clearly displayed throughout.

Outputs: {username}_kindred_spirit.json
"""

import json
import sys
from datetime import datetime
from pathlib import Path

# Import the dilemma system
sys.path.insert(0, str(Path(__file__).parent))
from Engine.kindred_spirit_calibration import (
    CalibrationSession,
    DilemmaCategory,
    UserResponse
)


class Colors:
    """ANSI color codes for terminal output"""
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    GRAY = '\033[90m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


def print_section(text, color=Colors.CYAN):
    """Print section header with color"""
    print(f"\n{color}{Colors.BOLD}{text}{Colors.RESET}\n")


def print_question(text, color=Colors.BLUE):
    """Print question with color"""
    print(f"{color}{text}{Colors.RESET}")


def print_note(text, color=Colors.GRAY):
    """Print subtle note/context"""
    print(f"{color}{text}{Colors.RESET}")


def get_input(prompt, color=Colors.GREEN):
    """Get user input with colored prompt"""
    return input(f"{color}{prompt}{Colors.RESET} ").strip()


def get_multiline_input(prompt):
    """Get multi-line input (end with empty line)"""
    print_question(prompt)
    print_note("(Press Enter twice when finished)")
    lines = []
    while True:
        line = input()
        if line == "" and lines:
            break
        lines.append(line)
    return "\n".join(lines).strip()


def get_choice(options, allow_other=True):
    """Get choice with validation"""
    # Convert options list to uppercase for validation
    valid_options = [opt.upper() for opt in options]
    options_str = '/'.join(valid_options)
    if allow_other:
        options_str += "/Other"
    
    while True:
        choice = get_input(f"Your choice ({options_str}):").upper()
        if choice in valid_options:
            return choice
        if choice in ['OTHER', 'O'] and allow_other:
            return 'OTHER'
        print_note(f"Please enter {options_str}")


def get_rating(prompt, scale=10):
    """Get numeric rating (1-10)"""
    while True:
        try:
            rating = int(get_input(f"{prompt} (1-{scale}):"))
            if 1 <= rating <= scale:
                return rating
            print_note(f"Please enter a number between 1 and {scale}")
        except ValueError:
            print_note("Please enter a valid number")


# ============================================================
# PHASE 4: RESONANT FIGURES (with graceful complexity)
# ============================================================

RESONANT_FIGURES = [
    {
        "name": "George Orwell",
        "appeal": "Intellectual honesty, clarity about truth and totalitarianism, 'Politics and the English Language'",
        "shadow": "Held views on race and homosexuality that were products of his time and class. His portrayal of women in novels is considered problematic by many readers.",
        "question": "Does Orwell's writing resonate with you despite these contradictions—or perhaps because he himself struggled with his own biases?"
    },
    {
        "name": "Marcus Aurelius",
        "appeal": "Stoic wisdom, discipline, acceptance of what can't be controlled, his Meditations on duty and compassion",
        "shadow": "Philosopher-king who preached compassion yet persecuted Christians and waged endless wars. Significant gap between ideals and actions.",
        "question": "Do his Meditations still guide you, knowing the distance between his principles and his reign?"
    },
    {
        "name": "Atticus Finch",
        "appeal": "Moral courage, standing alone for principle, compassionate justice in 'To Kill a Mockingbird'",
        "shadow": "In 'Go Set a Watchman' (sequel), revealed as attending a Klan meeting and holding segregationist views. Harper Lee later distanced herself from that portrayal.",
        "question": "Does the Atticus of 'Mockingbird' still represent something true about moral courage, regardless of the sequel's revelations?"
    },
    {
        "name": "Holden Caulfield",
        "appeal": "Radical authenticity vs. phoniness, protecting innocence, alienation as honest response to hypocrisy",
        "shadow": "Privileged teenager whose rebellion is enabled by wealth. His cynicism can be self-indulgent, his judgments of others harsh and unfair.",
        "question": "Does his critique of phoniness still ring true, even if his own position is privileged and sometimes hypocritical?"
    },
    {
        "name": "Ernest Hemingway",
        "appeal": "Authentic masculinity, courage under pressure, 'grace under pressure' prose style, lived adventurously",
        "shadow": "Toxic masculinity, cruelty to friends and wives, glorification of bullfighting/violence, deep misogyny, multiple failed marriages.",
        "question": "Does his prose still capture something true about courage and loss, despite how he treated people in his life?"
    },
    {
        "name": "Pablo Picasso",
        "appeal": "Revolutionary artist who shattered perspective, Guernica's anti-war power, relentless creative reinvention",
        "shadow": "Openly stated 'Women are machines for suffering.' Serially abused partners emotionally and financially. Marie-Thérèse Walter's daughter said he 'assassinated' her mother.",
        "question": "Can you admire Guernica's compassion while condemning how he treated women?"
    },
    {
        "name": "Mahatma Gandhi",
        "appeal": "Nonviolent resistance (Satyagraha) changed history, courage against British Empire, inspired MLK and Mandela",
        "shadow": "Early writings in South Africa expressed deeply racist views toward Black Africans. Problematic views on sexuality, caste. Treatment of his wife Kasturba was controlling and harsh.",
        "question": "Does Satyagraha's power transcend Gandhi's personal blind spots, or do those undermine the philosophy?"
    },
    {
        "name": "Steve Jobs",
        "appeal": "Visionary who changed computing, phones, music. 'Think Different,' obsessive attention to design, made technology beautiful",
        "shadow": "Cruel to colleagues, denied paternity of his daughter Lisa for years, parked in handicapped spots, took credit for others' work. Narcissism at pathological levels.",
        "question": "Does 'Think Different' still inspire, or does the messenger's narcissism poison the message?"
    },
    {
        "name": "John Lennon",
        "appeal": "'Imagine' and vision of peace, anti-war activism, vulnerability in songwriting, 'All You Need Is Love'",
        "shadow": "Sang 'Imagine no possessions' while living in the Dakota. Abusive to first wife Cynthia and son Julian (physical and emotional). Hypocrisy between message and life.",
        "question": "Does 'Imagine' still move you, despite Lennon's failure to live it?"
    },
    {
        "name": "Tyrion Lannister (Game of Thrones)",
        "appeal": "Intelligence over violence, empathy born from marginalization, wit as survival, pragmatic morality in brutal world",
        "shadow": "Fictional character, but his actions include murder (Shae, Tywin) driven by personal rage. His 'pragmatism' sometimes justifies cruelty. Drinks to escape rather than face pain.",
        "question": "Does his empathy still resonate, even when he acts from rage rather than principle?"
    },
    {
        "name": "Hannah Arendt",
        "appeal": "'Banality of evil,' thinking for yourself in totalitarian times, responsibility to question authority, brilliant political philosopher",
        "shadow": "Affair with Heidegger (her professor, who later joined Nazi party). Some argue she was too sympathetic to him post-war. Her coverage of Eichmann trial criticized by some as victim-blaming.",
        "question": "Does her analysis of totalitarianism still illuminate our moment, despite her complicated relationship with Heidegger?"
    },
    {
        "name": "Carl Sagan",
        "appeal": "Wonder + skepticism, 'Cosmos,' the 'pale blue dot,' science as candle in the dark, cosmic perspective on human conflicts",
        "shadow": "Neglected his children during his first marriages in pursuit of career. Admitted he was an absent father. His fame sometimes overshadowed collaborators' contributions.",
        "question": "Does the cosmic perspective still humble and inspire you, knowing he struggled to be present with his own family?"
    },
    {
        "name": "Katniss Everdeen (Hunger Games)",
        "appeal": "Survival, protecting family (Prim), distrust of propaganda, reluctant symbol, PTSD authentically portrayed",
        "shadow": "Fictional, but her violence (even if defensive) and manipulation by both sides raise questions. Ends up as tool of District 13's propaganda just as she was for the Capitol.",
        "question": "Does her protection of Prim still resonate, even though she ultimately becomes the symbol she resented?"
    },
    {
        "name": "Viktor Frankl",
        "appeal": "Meaning through suffering (logotherapy), choice even in concentration camps, 'Man's Search for Meaning,' refusal to be broken",
        "shadow": "Some historians question parts of his Holocaust narrative. His wife and mother died in camps—his survival when they didn't involves luck he couldn't control. Survivor's guilt shaped his philosophy.",
        "question": "Does his insight about meaning survive scrutiny of his narrative, or does it matter that he simplified complex trauma?"
    },
    {
        "name": "Ursula K. Le Guin",
        "appeal": "Questioned gender/power in 'The Left Hand of Darkness,' anarchism in 'The Dispossessed,' environmental ethics, 'late-stage capitalism' critique before it was cool",
        "shadow": "Early works ('Earthsea') had issues with race/representation she later acknowledged and tried to correct. Some argue her anarchism was more aesthetic than practical.",
        "question": "Does her questioning of power structures still challenge you, even if her early work reflected the biases of her era?"
    },
    {
        "name": "James Baldwin",
        "appeal": "Speaking truth about race ('The Fire Next Time'), complexity over comfort, love as political act, 'Not everything that is faced can be changed, but nothing can be changed until it is faced'",
        "shadow": "His sexuality and expatriate status led some Black Power activists to question his 'authenticity.' Malcolm X and Eldridge Cleaver attacked him. Struggled with alcohol.",
        "question": "Does his call for 'love as political act' still offer a path forward, even if it was rejected by more militant voices?"
    },
    {
        "name": "Aragorn (Lord of the Rings)",
        "appeal": "Reluctant leadership, duty over glory, humility despite destiny, ranger who becomes king, 'I would have followed you, my brother, my captain, my king'",
        "shadow": "Fictional, but represents aristocratic birthright as legitimacy. Inherited power, not earned. The 'rightful king' narrative is fundamentally anti-democratic.",
        "question": "Does his reluctant nobility still inspire, or is the 'rightful king' idea incompatible with your democratic values?"
    },
    {
        "name": "Fred Rogers",
        "appeal": "Kindness as radical act, emotional literacy for children (and adults), unconditional acceptance, 'You are special just the way you are'",
        "shadow": "His Christianity was gentle but real—some see religious framework as problematic. His affect (slow, deliberate) was performance, not his 'real' personality. Practiced what he preached, but it was work, not effortless sainthood.",
        "question": "Does his message of unconditional acceptance still comfort you, knowing it was disciplined practice rather than natural temperament?"
    },
    {
        "name": "Malala Yousafzai",
        "appeal": "Courage under violence (shot by Taliban), education as liberation, optimism despite trauma, youngest Nobel laureate",
        "shadow": "Young enough that her views are still forming—future evolution unknown. Some criticize her as Western media darling while other activists are ignored. Her platform is partly product of Western attention.",
        "question": "Does her advocacy for girls' education inspire you, even if her prominence is partly due to Western media amplification others don't receive?"
    },
    {
        "name": "Ellen Ripley (Alien)",
        "appeal": "Competence over ego, maternal protection (Newt), pragmatic vs. corporate greed, working-class hero who survives through intelligence",
        "shadow": "Fictional, but represents 'strong female character' trope that can be limiting. Her trauma (especially Alien 3 onward) is relentless—is that empowering or just suffering as spectacle?",
        "question": "Does her competent pragmatism still represent something true about courage, or is the Strong Female Character trope itself now problematic?"
    }
]


def print_progress(phase, current, total, phase_name):
    """Print progress bar and status"""
    percentage = int((current / total) * 100)
    bar_length = 40
    filled = int((current / total) * bar_length)
    bar = '█' * filled + '░' * (bar_length - filled)
    
    print(f"\n{Colors.CYAN}Phase {phase}: {phase_name}{Colors.RESET}")
    print(f"{Colors.GREEN}[{bar}] {current}/{total} ({percentage}%){Colors.RESET}")


def phase1_contemporary_dilemmas(session: CalibrationSession):
    """Phase 1: Contemporary political issues (15 dilemmas)"""
    
    print_section("═══════════════════════════════════════════════════════════════")
    print_section("PHASE 1: CONTEMPORARY ISSUES", Colors.CYAN)
    print_section("═══════════════════════════════════════════════════════════════")
    
    print("""
Let's start with issues from our current moment—politics, culture, technology.
These are the hot-button topics people argue about today.

There are no right answers. I'm not here to judge. I'm here to understand how
YOU think about these questions when the stakes feel real.
""")
    
    input(f"\n{Colors.GREEN}Press Enter to begin Phase 1...{Colors.RESET}")
    
    # Filter contemporary dilemmas
    contemporary = [d for d in session.dilemmas 
                   if d.category == DilemmaCategory.POLITICAL_CONTEMPORARY]
    
    responses = []
    
    for i, dilemma in enumerate(contemporary, 1):
        print_progress(1, i, len(contemporary), "Contemporary Issues")
        
        print_question(f"\n{dilemma.scenario}")
        print_note(f"A) {dilemma.option_a}")
        print_note(f"B) {dilemma.option_b}")
        if dilemma.option_other:
            print_note("Other) Something else")
        
        choice = get_choice(['A', 'B'], allow_other=dilemma.option_other)
        
        reasoning = get_multiline_input("\nWhat's your reasoning?")
        certainty = get_rating("How certain are you?", 10)
        emotional = get_rating("How emotionally charged was this?", 10)
        
        responses.append(UserResponse(
            dilemma_id=dilemma.id,
            choice=choice,
            reasoning=reasoning,
            certainty=certainty,
            emotional_weight=emotional
        ))
        
        print(f"\n{Colors.GREEN}Thank you.{Colors.RESET}")
    
    return responses


def phase2_timeless_dilemmas(session: CalibrationSession):
    """Phase 2: Timeless ethical questions (22 dilemmas)"""
    
    print_section("\n═══════════════════════════════════════════════════════════════")
    print_section("PHASE 2: TIMELESS ETHICS", Colors.CYAN)
    print_section("═══════════════════════════════════════════════════════════════")
    
    print("""
Thank you for exploring those contemporary issues with me.

Now I'd like to shift to questions humans have wrestled with for thousands
of years—questions that transcend our particular moment in history.

These are about abstract principles: honesty, justice, loyalty, the greater good.
""")
    
    input(f"\n{Colors.GREEN}Press Enter to begin Phase 2...{Colors.RESET}")
    
    # Filter timeless dilemmas (exclude contemporary and existential)
    timeless = [d for d in session.dilemmas 
               if d.category not in [DilemmaCategory.POLITICAL_CONTEMPORARY,
                                    DilemmaCategory.PERSONAL_EXISTENTIAL]]
    
    responses = []
    
    for i, dilemma in enumerate(timeless, 1):
        print_progress(2, i, len(timeless), "Timeless Ethics")
        
        print_question(f"\n{dilemma.scenario}")
        print_note(f"A) {dilemma.option_a}")
        print_note(f"B) {dilemma.option_b}")
        if dilemma.option_other:
            print_note("Other) Something else")
        
        choice = get_choice(['A', 'B'], allow_other=dilemma.option_other)
        
        reasoning = get_multiline_input("\nWhat's your reasoning?")
        certainty = get_rating("How certain are you?", 10)
        emotional = get_rating("How emotionally charged was this?", 10)
        
        responses.append(UserResponse(
            dilemma_id=dilemma.id,
            choice=choice,
            reasoning=reasoning,
            certainty=certainty,
            emotional_weight=emotional
        ))
        
        print(f"\n{Colors.GREEN}Thank you.{Colors.RESET}")
    
    return responses


def phase3_existential_dilemmas(session: CalibrationSession):
    """Phase 3: Personal/existential questions (2+ dilemmas)"""
    
    print_section("\n═══════════════════════════════════════════════════════════════")
    print_section("PHASE 3: PERSONAL & EXISTENTIAL", Colors.CYAN)
    print_section("═══════════════════════════════════════════════════════════════")
    
    print("""
We've explored abstract ethical principles. Now I want to ask about the most
personal questions—about YOU, your loved ones, your own mortality and meaning.

These aren't political. They're not about strangers. They're about what matters
to you when everything else falls away.
""")
    
    input(f"\n{Colors.GREEN}Press Enter to begin Phase 3...{Colors.RESET}")
    
    # Filter existential dilemmas
    existential = [d for d in session.dilemmas 
                  if d.category == DilemmaCategory.PERSONAL_EXISTENTIAL]
    
    responses = []
    
    for i, dilemma in enumerate(existential, 1):
        print_progress(3, i, len(existential), "Personal & Existential")
        
        print_question(f"\n{dilemma.scenario}")
        print_note(f"A) {dilemma.option_a}")
        print_note(f"B) {dilemma.option_b}")
        if dilemma.option_other:
            print_note("Other) Something else")
        
        choice = get_choice(['A', 'B'], allow_other=dilemma.option_other)
        
        reasoning = get_multiline_input("\nWhat's your reasoning?")
        certainty = get_rating("How certain are you?", 10)
        emotional = get_rating("How emotionally charged was this?", 10)
        
        responses.append(UserResponse(
            dilemma_id=dilemma.id,
            choice=choice,
            reasoning=reasoning,
            certainty=certainty,
            emotional_weight=emotional
        ))
        
        print(f"\n{Colors.GREEN}Thank you.{Colors.RESET}")
    
    return responses


def phase4_resonant_figures():
    """Phase 4: Explore heroes with graceful honesty about their flaws"""
    
    print_section("\n═══════════════════════════════════════════════════════════════")
    print_section("PHASE 4: RESONANT FIGURES - Show Me Your Heroes", Colors.CYAN)
    print_section("═══════════════════════════════════════════════════════════════")
    
    print("""
We've explored abstract dilemmas. Now let's talk about people—real and fictional—
who shaped how you think about the world.

Here's what's interesting: The people we admire are never simple. Gandhi preached
nonviolence but held racist views early in life. Hemingway wrote beautifully about
courage but was cruel to those closest to him. Atticus Finch stood against racism
in one book and attended Klan meetings in the sequel.

This isn't about canceling anyone. It's about something deeper: Can we hold both
truths? The wisdom AND the humanity? The inspiration AND the hypocrisy?

Your answer reveals a lot about how you handle moral complexity.
""")
    
    input(f"\n{Colors.GREEN}Press Enter to begin Phase 4...{Colors.RESET}")
    
    responses = []
    
    # Show all 20 figures
    for i, figure in enumerate(RESONANT_FIGURES, 1):
        print_progress(4, i, len(RESONANT_FIGURES), "Resonant Figures")
        
        print_question(f"\n{Colors.BOLD}{figure['name']}{Colors.RESET}")
        print(f"\n{Colors.BLUE}Why people connect:{Colors.RESET}")
        print(f"  {figure['appeal']}")
        
        print(f"\n{Colors.GRAY}The complexity:{Colors.RESET}")
        print(f"  {figure['shadow']}")
        
        print(f"\n{Colors.CYAN}{figure['question']}{Colors.RESET}\n")
        
        # Does this figure resonate?
        resonates = get_input("Does this figure resonate with you? (yes/no/skip):").lower()
        
        if resonates in ['y', 'yes']:
            # What specifically?
            what_resonates = get_multiline_input(
                f"\nWhat about {figure['name']} speaks to you?"
            )
            
            # How do they handle the shadow?
            print_question(f"\nKnowing {figure['name']}'s flaws, how do you hold this?")
            print_note("A) Reject them entirely (flaws invalidate the work)")
            print_note("B) Separate art from artist (wisdom transcends the person)")
            print_note("C) Hold both truths (flawed people can produce insight)")
            print_note("D) It depends on severity")
            
            handling = get_choice(['A', 'B', 'C', 'D'], allow_other=False)
            
            # Certainty
            certainty = get_rating("\nHow certain are you about this position?", 10)
            
            responses.append({
                "figure": figure['name'],
                "resonates": True,
                "what_resonates": what_resonates,
                "shadow_handling": handling,
                "certainty": certainty,
                "timestamp": datetime.now().isoformat()
            })
            
            print(f"\n{Colors.GREEN}Thank you for that thoughtful reflection.{Colors.RESET}")
        
        elif resonates in ['n', 'no']:
            why_not = get_input(f"\nWhat doesn't work for you about {figure['name']}? (optional):")
            responses.append({
                "figure": figure['name'],
                "resonates": False,
                "why_not": why_not if why_not else None,
                "timestamp": datetime.now().isoformat()
            })
        
        # Continue?
        if i < len(RESONANT_FIGURES):
            continue_choice = get_input(f"\nContinue to next figure? (yes/no, {len(RESONANT_FIGURES)-i} remaining):").lower()
            if continue_choice in ['n', 'no']:
                print_note("\nThat's fine. Moving to summary...")
                break
    
    return responses


# ============================================================
# PHASE 5: ETHICAL FRAMEWORKS (with extreme examples)
# ============================================================

ETHICAL_FRAMEWORKS = [
    {
        "name": "Utilitarianism",
        "summary": "The right action is whatever produces the greatest good for the greatest number. Outcomes matter, not intentions.",
        "example": "A surgeon could kill one healthy patient to harvest organs and save five dying patients. Utilitarian math says: 5 lives > 1 life, so do it.",
        "real_world": "Harry Truman's decision to drop atomic bombs on Hiroshima and Nagasaki (1945): Kill ~200,000 Japanese civilians to end the war and save potentially millions of lives (Allied invasion of Japan). Pure utilitarian calculus.",
        "question": "Does this match how you actually make decisions, or does it feel wrong despite the math?"
    },
    {
        "name": "Deontology (Kant)",
        "summary": "Some actions are simply wrong, regardless of outcome. Lying is wrong even if it saves lives. Duty and rules matter more than consequences.",
        "example": "Nazi at your door asks if you're hiding Jews. Deontology says: lying is wrong, so you must tell the truth even if it means their deaths.",
        "real_world": "The Nuremberg Trials (1945-46): Nazi defendants argued 'I was following orders' (consequentialist excuse). Prosecutors argued: some acts (genocide) are wrong regardless of authority or outcome. Duty to refuse immoral orders.",
        "question": "Do you believe some rules are absolute, or does context always matter?"
    },
    {
        "name": "Virtue Ethics (Aristotle)",
        "summary": "Focus on character, not rules or outcomes. Ask: 'What would a good person do?' Cultivate virtues like courage, wisdom, compassion.",
        "example": "Your friend is in a self-destructive spiral. Virtue ethics asks: does compassion mean enabling them (kindness) or confronting them (courage)? There's no formula—what does a wise, caring person do here?",
        "real_world": "Nelson Mandela's release from prison (1990): He could have led violent retribution against apartheid oppressors. Instead, chose reconciliation. Not rule-based, not utilitarian—it was character: wisdom, forgiveness, long-term vision of who he wanted to be.",
        "question": "Do you think morality is about building good character over time, or following principles?"
    },
    {
        "name": "Care Ethics",
        "summary": "Morality grows from relationships and empathy, not abstract principles. Caring for specific people you're connected to matters more than universal rules.",
        "example": "Your child and a stranger's child are both drowning. You can only save one. Care ethics says: save your child. The relationship creates the obligation, not abstract equality.",
        "real_world": "The Tuskegee Syphilis Study (1932-1972): Abstract 'greater good' (scientific knowledge) trumped care for actual Black men suffering. Care ethics would say: these are real people with families who trust you—relationship obligations override abstract research value.",
        "question": "Do you believe special relationships create special obligations that override impartial fairness?"
    },
    {
        "name": "Egoism",
        "summary": "The right action is whatever serves your rational self-interest. Not hedonism or cruelty—enlightened self-interest recognizes that cooperation, reputation, and integrity often serve you best.",
        "example": "You witness a crime. Reporting it risks retaliation and wastes your time. Egoism asks: does reporting serve YOUR interests (safety, social contract, reputation)? If not, walk away.",
        "real_world": "Wall Street traders before 2008 crash: Knew subprime mortgages were toxic but sold them anyway. Short-term rational self-interest (bonuses, profits). Didn't work long-term (crash hurt everyone). Reveals difference between narrow vs. enlightened egoism.",
        "question": "Do you believe pursuing your own interests is not just acceptable but the foundation of a functioning society?"
    },
    {
        "name": "Altruism",
        "summary": "The right action is whatever serves others, even at cost to yourself. Self-sacrifice for the greater good is the highest moral calling.",
        "example": "You have a rare blood type. Donating bone marrow monthly would save children's lives but cause you significant pain and inconvenience. Altruism says: your comfort matters less than their lives—donate.",
        "real_world": "Dr. Paul Farmer (Partners in Health, 1980s-2022): Spent decades treating poor in Haiti/Rwanda, living in harsh conditions, earning far below his potential. Radical altruism: 'The idea that some lives matter less is the root of all that's wrong with the world.'",
        "question": "Do you believe self-sacrifice for others is morally required, or is it supererogatory (admirable but not obligatory)?"
    },
    {
        "name": "Contractarianism",
        "summary": "Morality is a social contract—rules we agree to for mutual benefit. Right and wrong are whatever people in a society agree upon.",
        "example": "In a society where everyone agrees that assisted suicide is acceptable, it's moral. In a society where everyone opposes it, it's immoral. There's no objective truth—only what the contract says.",
        "real_world": "Roe v. Wade overturned (2022): Reveals contractarian logic. Abortion rights aren't 'natural' or 'objective'—they're whatever the social contract (Constitution, state laws) says. When contract changes, morality changes. No external truth to appeal to.",
        "question": "Do you believe morality is ultimately just what we agree upon, or are there objective truths beyond social consensus?"
    },
    {
        "name": "Natural Law (Aquinas)",
        "summary": "Morality is built into the nature of things—God or reason designed the universe with inherent purposes. Actions aligned with natural purposes are good; violations are wrong.",
        "example": "Contraception is wrong because it violates the natural purpose of sex (procreation). Same-sex relationships are wrong for the same reason. Natural law says: purposes are built-in, not chosen.",
        "real_world": "Catholic Church's response to AIDS crisis (1980s-90s): Refused to endorse condoms despite millions dying. Natural law argument: contraception violates sex's natural purpose, so even to save lives, it's wrong. Purpose > consequences.",
        "question": "Do you believe there are inherent purposes to things, or do we create meaning and purpose ourselves?"
    },
    {
        "name": "Existentialist Ethics (Sartre)",
        "summary": "There are no pre-existing moral rules. You are 'condemned to be free'—you must create meaning through authentic choices. Responsibility is total and inescapable.",
        "example": "You must choose whether to care for your dying mother or join the Resistance against Nazis. There's no right answer—you create meaning through the choice. But you can't escape responsibility for what you choose.",
        "real_world": "Vietnam War draft resisters (1960s-70s): No authority (government, church, tradition) could tell them the war was just or unjust. They had to choose: serve or resist. Either way, radical responsibility for the choice and its consequences (prison, exile, combat).",
        "question": "Do you believe you are radically free to create your own values, or do you look to external sources (tradition, religion, reason) for guidance?"
    },
    {
        "name": "Ubuntu ('I am because we are')",
        "summary": "Personhood is communal—you exist through relationships. Morality is about sustaining community and interconnection. Harmony and restoration matter more than punishment.",
        "example": "Someone harms you. Ubuntu asks: what restores the community? Not 'what punishes the wrongdoer' but 'what heals the break in our web of relationships?' Forgiveness may serve justice better than punishment.",
        "real_world": "South Africa's Truth and Reconciliation Commission (1996-1998): After apartheid, didn't pursue Nuremberg-style trials. Ubuntu logic: punishment fractures further. Instead, truth-telling + amnesty to restore social fabric. 'I am human because you are human.'",
        "question": "Do you believe justice is primarily about restoring relationships, or about individual accountability and consequences?"
    },
    {
        "name": "Stoicism (Marcus Aurelius, Epictetus)",
        "summary": "Focus on what you can control (your thoughts, actions, responses). Accept what you can't control (others, fate, death). Virtue is the only good; external things are 'preferred indifferents.'",
        "example": "Your business fails due to economic collapse (not your fault). Stoicism says: you don't control the economy, so don't rage at it. You control your response—find meaning in adversity, rebuild with discipline, accept loss with equanimity.",
        "real_world": "James Stockdale, Vietnam POW (1965-1973): Tortured for 7+ years. Used Stoic principles (Epictetus): 'I never lost faith in the end of the story... but I also confronted the brutal facts.' Controlled his mind when his body was broken. Acceptance + will.",
        "question": "Do you believe acceptance of what you can't control is wisdom, or is it resignation that enables injustice?"
    },
    {
        "name": "Pragmatism (William James, Dewey)",
        "summary": "Truth and morality are what 'works'—what produces good outcomes in practice. No abstract principles; test ideas by their consequences in real life.",
        "example": "A lie to your dying father ('You were a great dad') makes his last days peaceful, while the truth ('You were absent and it hurt') serves no purpose. Pragmatism says: what works here is the lie.",
        "real_world": "FDR's New Deal (1933-1939): Didn't ask 'is government intervention in markets morally right in theory?' Asked: 'Does Social Security work? Does it reduce suffering?' Pragmatism: test policies by results, not ideology. Abandon what fails, keep what works.",
        "question": "Do you believe truth and morality are what produces good results in practice, or are there principles that matter regardless of outcomes?"
    },
    {
        "name": "Moral Particularism",
        "summary": "Every situation is unique. Moral rules don't reliably transfer across contexts. You must read each situation holistically—what's right here may be wrong there.",
        "example": "Lying: wrong to your spouse about an affair, but right to Nazis at your door. There's no rule 'lying is wrong' that holds across cases. Context is everything; principles mislead.",
        "real_world": "Obama's decision to kill Anwar al-Awlaki (2011): American citizen, no trial, killed by drone. Couldn't apply simple rule ('citizens get trials'). Context mattered: he was in Yemen, actively planning attacks, unreachable by law enforcement. Particularist logic: this case is unique.",
        "question": "Do you think 'it depends' is wisdom or evasion? Can moral rules guide us, or is every case truly unique?"
    },
    {
        "name": "Rights-Based Ethics",
        "summary": "Individuals have fundamental rights (speech, privacy, self-defense, property) that cannot be violated even for the greater good. Rights create absolute boundaries.",
        "example": "Free speech is a right. Even if banning hate speech would reduce harm (utilitarian win) and most people support it (social contract), it violates rights. Rights trump both outcomes and consensus.",
        "real_world": "ACLU defending Nazis' right to march in Skokie, Illinois (1977): Holocaust survivors lived there. March would cause immense pain. But 1st Amendment is a right—content-neutral. ACLU argued: rights don't bend for consequences or offense. (They won; march happened.)",
        "question": "Do you believe rights are inviolable boundaries, or are they weighed against other concerns (safety, harm, community)?"
    },
    {
        "name": "Divine Command Theory",
        "summary": "Right and wrong are defined by God's will. Morality = obedience to divine authority. Without God, there is no objective moral truth—just human preference.",
        "example": "If God commanded Abraham to sacrifice Isaac, it was moral—not because of outcomes or character, but because God commanded it. Obedience to divine will is the foundation of all morality.",
        "real_world": "Kim Davis refusing marriage licenses to gay couples (2015): 'God's authority' trumped Supreme Court ruling and civil law. Divine command logic: human laws (even Constitutional ones) are subordinate to God's law. Morality isn't negotiable or contextual.",
        "question": "Do you believe morality requires a divine source, or can it exist independently of religious authority?"
    },
    {
        "name": "Moral Pluralism (Isaiah Berlin)",
        "summary": "Multiple values are real and sometimes irreducibly in conflict. Liberty vs. equality, justice vs. mercy—no higher principle resolves them. Tragic choices are real; you sometimes just lose something.",
        "example": "Justice demands the murderer be punished. Mercy demands forgiveness for their traumatic childhood. Both are real values. There's no formula to 'reconcile' them—you must choose, and you lose something either way. Tragedy is real.",
        "real_world": "COVID lockdowns (2020-2021): Public health (save lives) vs. liberty (freedom of movement) vs. economic survival (livelihoods). These aren't fake conflicts with a 'correct' answer. They're real value conflicts. Any choice sacrifices something precious. Pluralism: tragic choices are unavoidable.",
        "question": "Do you believe value conflicts can always be resolved by a higher principle, or are some conflicts irreducibly tragic?"
    }
]


def phase5_ethical_frameworks():
    """Phase 5: Established ethical frameworks with extreme examples"""
    
    print_section("\n═══════════════════════════════════════════════════════════════")
    print_section("PHASE 5: ETHICAL FRAMEWORKS - How Do You Actually Decide?", Colors.CYAN)
    print_section("═══════════════════════════════════════════════════════════════")
    
    print("""
Philosophers have spent thousands of years trying to answer: "How should we live?"

Here are the major frameworks they've developed. Each has passionate defenders.
Each has serious problems. None is obviously right.

What's interesting isn't which one is "correct"—it's which one matches how you
ACTUALLY make decisions, not how you think you should.

For each framework, I'll give you a hypothetical example and a real historical
event to test whether it really fits your intuitions.
""")
    
    input(f"\n{Colors.GREEN}Press Enter to begin Phase 5...{Colors.RESET}")
    
    responses = []
    
    for i, framework in enumerate(ETHICAL_FRAMEWORKS, 1):
        print_progress(5, i, len(ETHICAL_FRAMEWORKS), "Ethical Frameworks")
        
        print_question(f"\n{Colors.BOLD}{framework['name']}{Colors.RESET}")
        
        print(f"\n{Colors.BLUE}Core idea:{Colors.RESET}")
        print(f"  {framework['summary']}")
        
        print(f"\n{Colors.GRAY}Hypothetical example:{Colors.RESET}")
        print(f"  {framework['example']}")
        
        print(f"\n{Colors.YELLOW}Real-world event (last 70 years):{Colors.RESET}")
        print(f"  {framework['real_world']}")
        
        print(f"\n{Colors.CYAN}{framework['question']}{Colors.RESET}\n")
        
        # Does this match their intuitions?
        print_note("A) This matches how I actually decide things")
        print_note("B) I want to believe this, but I don't actually live it")
        print_note("C) This feels wrong/incomplete to me")
        print_note("D) I'm not sure / need to think about it")
        
        response = get_choice(['A', 'B', 'C', 'D'], allow_other=False)
        
        # If A or B, ask for elaboration
        if response in ['A', 'B']:
            elaboration = get_multiline_input(
                f"\nWhat about {framework['name']} resonates with you?"
            )
        else:
            elaboration = None
        
        # If C, ask what's wrong
        if response == 'C':
            objection = get_multiline_input(
                f"\nWhat feels wrong or incomplete about {framework['name']}?"
            )
        else:
            objection = None
        
        responses.append({
            "framework": framework['name'],
            "response": response,
            "elaboration": elaboration,
            "objection": objection,
            "timestamp": datetime.now().isoformat()
        })
        
        # Continue?
        if i < len(ETHICAL_FRAMEWORKS):
            print()  # Blank line before next
    
    return responses


def save_results(username, phase1_data, phase2_data, phase3_data, phase4_data, phase5_data):
    """Save calibration results to JSON file"""
    output_dir = Path("pepper_settings/calibration_results")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    filename = output_dir / f"{username}_kindred_spirit.json"
    
    # Convert UserResponse dataclass instances to dicts
    def response_to_dict(r):
        if hasattr(r, '__dict__'):
            return r.__dict__
        return r
    
    output = {
        "username": username,
        "calibration_date": datetime.now().isoformat(),
        "version": "1.0_full_five_phases",
        "phase1_contemporary": [response_to_dict(r) for r in phase1_data],
        "phase2_timeless": [response_to_dict(r) for r in phase2_data],
        "phase3_existential": [response_to_dict(r) for r in phase3_data],
        "phase4_resonant_figures": phase4_data,
        "phase5_ethical_frameworks": phase5_data,
        "summary": {
            "total_questions": len(phase1_data) + len(phase2_data) + len(phase3_data) + len(phase4_data) + len(phase5_data),
            "phase1_count": len(phase1_data),
            "phase2_count": len(phase2_data),
            "phase3_count": len(phase3_data),
            "phase4_count": len(phase4_data),
            "phase5_count": len(phase5_data)
        }
    }
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    return filename


def main():
    """Main calibration flow"""
    print_section("═══════════════════════════════════════════════════════════════")
    print_section("    KINDRED SPIRIT CALIBRATION", Colors.CYAN)
    print_section("═══════════════════════════════════════════════════════════════")
    
    print(f"""
This is not a test. There are no right answers.

This is a conversation to help discover your actual values—not the ones you think
you should have, but the ones you actually live by.

{Colors.BOLD}The full experience has 5 phases (~75 questions):{Colors.RESET}

  Phase 1: Contemporary political issues (15 questions)
  Phase 2: Timeless ethical dilemmas (22 questions)
  Phase 3: Personal & existential (2+ questions)
  Phase 4: Resonant figures - heroes with flaws (20 figures)
  Phase 5: Ethical frameworks (16 frameworks)

You can exit anytime with Ctrl+C. Your progress will be saved.
""")
    
    username = get_input("\nWhat should I call you?")
    if not username:
        username = "anonymous"
    
    print(f"\n{Colors.GREEN}Hello, {username}.{Colors.RESET}")
    print("\nLet's begin.\n")
    
    input(f"{Colors.GREEN}Press Enter to start...{Colors.RESET}")
    
    # Initialize calibration session
    session = CalibrationSession()
    
    # Phase 1: Contemporary dilemmas
    phase1_data = phase1_contemporary_dilemmas(session)
    
    # Phase 2: Timeless dilemmas
    phase2_data = phase2_timeless_dilemmas(session)
    
    # Phase 3: Existential dilemmas
    phase3_data = phase3_existential_dilemmas(session)
    
    # Phase 4: Resonant figures
    phase4_data = phase4_resonant_figures()
    
    # Phase 5: Ethical frameworks
    phase5_data = phase5_ethical_frameworks()
    
    # Save results
    print_section("\n═══════════════════════════════════════════════════════════════")
    print_section("Saving your responses...", Colors.CYAN)
    
    output_file = save_results(username, phase1_data, phase2_data, phase3_data, phase4_data, phase5_data)
    
    print(f"\n{Colors.GREEN}✓ Saved to: {output_file}{Colors.RESET}")
    
    # Summary
    total_dilemmas = len(phase1_data) + len(phase2_data) + len(phase3_data)
    resonated_count = sum(1 for r in phase4_data if r.get('resonates'))
    framework_matches = sum(1 for r in phase5_data if r['response'] in ['A', 'B'])
    
    print(f"""
{Colors.BOLD}SESSION COMPLETE{Colors.RESET}

{Colors.CYAN}Phase 1 (Contemporary):{Colors.RESET} {len(phase1_data)} dilemmas answered
{Colors.CYAN}Phase 2 (Timeless):{Colors.RESET} {len(phase2_data)} dilemmas answered
{Colors.CYAN}Phase 3 (Existential):{Colors.RESET} {len(phase3_data)} dilemmas answered
{Colors.CYAN}Phase 4 (Figures):{Colors.RESET} Connected with {resonated_count} out of {len(phase4_data)} figures
{Colors.CYAN}Phase 5 (Frameworks):{Colors.RESET} Resonated with {framework_matches} out of {len(phase5_data)} frameworks

{Colors.CYAN}Total responses:{Colors.RESET} {total_dilemmas + len(phase4_data) + len(phase5_data)}

{Colors.BOLD}What happens next?{Colors.RESET}

This JSON file captures your responses. Future versions will analyze patterns:
  • Do you reject flawed heroes entirely? (purity vs. pragmatism)
  • Do you separate art from artist? (wisdom transcends person)
  • Do you hold contradictions? (both/and vs. either/or thinking)
  • Which flaws are forgivable, which aren't? (your actual hierarchy of values)
  • Which ethical frameworks match your actual decision-making?
  • Where do stated ideals diverge from lived values?

This is the beginning of building your Kindred Spirit—an AI that reflects
YOUR values, not some corporate training set's values.

Not paternalism. Partnership.
""")
    
    print(f"\n{Colors.GREEN}Thank you, {username}.{Colors.RESET}\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Calibration interrupted. Partial results may be saved.{Colors.RESET}\n")
        sys.exit(0)
