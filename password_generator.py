
import secrets
import string


# In[18]:


# 1. Put your favorite quotes here, grouped by show
SHOW_QUOTES = {
    "Psych": [
        "I've heard it both ways.",
        "Suck it!",
        "You know that's right.",
        "Come on, son!",
        "I don't lose things. I place things in locations which later elude me.",
        "Just because you put syrup on something don't make it pancakes.",
        "Do i need to slap you in the face?",
        "Hes mr black and im mr tan.",
        "Wait for it!"
    ],

    "Batman Beyond": [
        "Every time I put on that suit, it's my chance to help people who are in trouble.",
        "I am Batman.",
        "Sometimes I ask myself if Batman is the suit or the man inside it.",
        "One night always makes the difference.",
        "Is Batman the suit or the man inside it?"
    ],

    "Limitless": [
        "You remember a lot more than you think you do.",
        "Just because you remember everything doesn't mean you know everything.",
        "On NZT, everything is connected.",
        "My brain is running a thousand miles an hour.",
        "This pill lets you access all of it."
    ],

    "Smallville": [
        "Whatever you are, whatever you're planning, I'm going to stop you.",
        "I just want to be normal.",
        "That's your destiny, Clark. To help people.",
        "You have no idea what I'm capable of.",
        "You can't deny who you really are.",
        "You were sent here for a reason."
    ],

    "No Game No Life": [
        "Checkmate.",
        "We do not play to lose.",
        "In this world, weakness is not a sin.",
        "You have to make your own way.",
        "As long as we’re together, we can win any game.",
        "The strong polish their fangs, the weak polish their wisdom."
    ],

    "No Game No Life Zero": [
        "I will not let this world fall to despair.",
        "We will carve a future from this war.",
        "As long as you live, hope lives with you.",
        "Even in a world of ruin, love can bloom.",
        "This is our final gambit.",
        "We fight for a tomorrow we've never seen."
    ],

    "Fairy Tail": [
        "We are Fairy Tail!",
        "I will never give up on my friends!",
        "Feel the power of our bonds!",
        "If we don't have the power to protect our friends, then what is the point of anything?",
        "I’ll show you the power of a guild!",
        "Do fairies really have tails? Who knows! But it’s a mystery that fills our hearts!"
    ],

    "Rising of the Shield Hero": [
        "I am the Shield Hero.",
        "I will protect them, no matter what.",
        "A hero rises from the bottom.",
        "I won't trust anyone again… not blindly.",
        "This shield is my only weapon, and it is enough.",
        "I will stand my ground, even if the world hates me."
    ],

    "Dr Stone": [
        "Get excited!",
        "Ten billion percent science!",
        "Science will save humanity.",
        "The key to victory is science!",
        "We’re going to rebuild civilization from scratch!",
        "If it's impossible, then science will make it possible!"
    ],

    "Yugioh": [
        "It’s time to duel!",
        "Heart of the cards, guide me!",
        "You activated my trap card!",
        "My move!",
        "I believe in my deck.",
        "Your fate is sealed!"
    ],

    "Teen Titans": [
        "Titans, go!",
        "Booyah!",
        "The Teen Titans never quit.",
        "We're stronger together.",
        "Azarath Metrion Zinthos.",
        "The night is always darkest before the dawn — unless you're me."
    ],

    "Young Justice": [
        "Get whelmed.",
        "Recognized.",
        "We're not sidekicks.",
        "Pretty sure the feeling is mutual.",
        "We are the Justice League’s secret weapon.",
        "Just stay calm. Or at least pretend you are.",
        "Feel the aster",
        "Why isnt anyone ever just whelmed?"
    ],

    "From Commonplace to World's Strongest": [
        "I'll survive this hell.",
        "Weakness won’t stop me anymore.",
        "I forge my own destiny.",
        "I won't die here.",
        "I make my own path now.",
        "I’ll crush anyone who stands in my way."
    ],

    "Your Lie in April": [
        "Music is freedom.",
        "Spring will come again.",
        "You exist in a world of color.",
        "People can change.",
        "Even so, I still want to keep playing.",
        "You're the reason I can move forward.",
        "I like Tsubaka"
    ],

    "Ben 10": [
        "It's hero time!",
        "I've got ten aliens and counting.",
        "Time to turn things up a notch.",
        "Never underestimate the Omnitrix.",
        "You mess with me, you get the aliens.",
        "I always figure something out.",
        "Its about you knowing you did the right thing."
    ],

    "Danny Phantom": [
        "I'm going ghost!",
        "You don't stand a ghost of a chance.",
        "I'm half ghost, not helpless.",
        "My powers are a part of me.",
        "I guess the future isn't as set in stone as you think it is.",
        "Maybe that's all anybody needs a second chance.",
        "I don't have to win i just have to make sure you lose!"
    ],

    "SAO": [
        "This is not a game anymore.",
        "I will clear this world.",
        "I will protect you, Asuna.",
        "Surviving is winning.",
        "In this world, you fight to live.",
        "A true player never gives up.",
        "a single blade can take you anywhere you want to go",
        "Rather than leaving someone to die, I'd much rather die together with them"
    ],

    "Gravity Falls": [
        "Trust no one.",
        "Reality is an illusion.",
        "Get ready for weirdness.",
        "Memories fade but weirdness lasts forever.",
        "It's funny how dumb you are!",
        "Everything's connected."
    ],

    "Star vs the Forces of Evil": [
        "I'm a magical princess from another dimension!",
        "You can’t spell Star without trouble.",
        "A little magic never hurt anyone right?",
        "This dimension is weird.",
        "Let’s make some chaos!"
    ],

    "The Batman 2004": [
        "I am the night.",
        "Justice never sleeps.",
        "Gotham needs me.",
        "Fear is a powerful tool.",
        "The Batman works alone.",
        "I don’t give up."
    ],

    "Batman The Brave and the Bold": [
        "Outrageous!",
        "Crime never sleeps and neither do I.",
        "Heroes unite!",
        "Justice always prevails.",
        "We’re stronger together, hero.",
        "Gotham can't handle all this boldness."
    ],

    "Ben 10 Omniverse": [
        "Hero time, all the time.",
        "New look, same hero.",
        "The Omnitrix never fails.",
        "Time to switch it up.",
        "Being a hero never gets old.",
        "I'm still Ben 10!"
    ],

    "Ben 10 Alien Force": [
        "The universe still needs heroes.",
        "We don’t give up.",
        "I've grown up, so have my enemies.",
        "Stronger than ever.",
        "Hero time doesn’t end.",
        "Let's save the universe."
    ],

    "Ben 10 Ultimate Alien": [
        "Ultimate power, ultimate responsibility.",
        "Time to go ultimate.",
        "Heroes evolve.",
        "I'm just getting started.",
        "The Omnitrix is limitless.",
        "I’m the ultimate hero."
    ],

    "Fruit of Grisaia": [
        "Everyone carries their own scars.",
        "I walk my own path.",
        "A heart can be broken and still move forward.",
        "The past shapes us, but doesn’t chain us.",
        "Even broken people can start again.",
        "I won’t run from myself anymore."
    ],

    "Regular Show": [
        "It’s anything but.",
        "Stop talking and start working.",
        "OOOOOOOOOOH!",
        "You know who else did that? MY MOM!",
        "This is getting way too regular.",
        "Dude, what even is today?",
        "Sometimes you've got to go insane to out-sane the sane."
    ],

    "Bufori": [
        "Destinies collide in strange ways.",
        "We all have our part to play.",
        "Strength comes from hardship.",
        "Heroes aren’t born, they’re tested.",
        "The path forward isn’t always clear."
    ],

    "Charlotte": [
        "Power comes with a price.",
        "Your choices define you.",
        "We’re stronger together.",
        "Even broken wings can fly again.",
        "I won't let fate control me.",
        "The world changes one decision at a time."
    ],

    "Craig of the Creek": [
        "The creek is our kingdom.",
        "Every adventure starts with a step.",
        "We make the rules down here.",
        "This place is for everyone.",
        "Imagination makes everything real.",
        "The creek never lets you down."
    ],

    "DC Legends of Tomorrow": [
        "We’re the misfits, not the heroes.",
        "Changing history is what we do.",
        "Time needs us — even if it doesn’t want us.",
        "We’re legends for a reason.",
        "We don’t follow fate; we rewrite it.",
        "Someone’s gotta fix the timeline."
    ],

    "The Arrow": [
        "You have failed this city.",
        "I made a promise to protect it.",
        "I’m not the hero you wanted. I’m the one you have.",
        "Survival is not enough — we must save others.",
        "Justice comes with a cost.",
        "I became something else. I became someone else."
    ],

    "The Flash": [
        "I am the fastest man alive.",
        "Run, Barry, run!",
        "Sometimes the only way forward is to run.",
        "Heroes save people. Legends change the world.",
        "You can’t outrun destiny.",
        "Believe in the impossible."
    ],
    
    "The Misfits of Demon Academy": [
        "Did you really think that would kill me?",
        "Only one truth matters: I am Anos Voldigoad.",
        "A king needs no throne.",
        "Do not mistake arrogance for power.",
        "I reincarnated to end this conflict.",
        "Your rules do not apply to me."
    ],

    "Scooby Doo Mystery Inc": [
        "Jinkies!",
        "Zoinks!",
        "Looks like we’ve got a mystery to solve.",
        "Would you do it for a Scooby Snack?",
        "Let’s split up and search for clues.",
        "There’s more to this mystery than meets the eye."
    ],

    "What's New Scooby Doo": [
        "What’s new, Scooby-Doo?",
        "We’re coming after you!",
        "I think we’ve got a mystery to solve.",
        "Jeepers!",
        "Scooby-Doo, where are you?",
        "We’re on the case and tracking you down."
    ],

    "The Hollow": [
        "The game isn’t what it seems.",
        "We have to work together.",
        "Not everything here follows the rules.",
        "This world is a puzzle.",
        "Think fast or fall behind.",
        "The truth is hidden in plain sight."
    ],

    "Trollhunters": [
        "For the glory of Merlin, Daylight is mine to command!",
        "You are stronger than you think.",
        "Evil never sleeps.",
        "Destiny chooses us.",
        "I will protect both worlds.",
        "Courage comes from the heart."
    ],

    "Wizards": [
        "Magic is a responsibility.",
        "The arcane flows through everything.",
        "Knowledge is the greatest spell.",
        "Power must be earned, not taken.",
        "The veil between worlds is thin.",
        "A wizard’s path is never simple."
    ],

    "Seven Deadly Sins": [
        "I’ll bear your sins.",
        "We will protect the kingdom.",
        "Have faith in the captain!",
        "I’ll never abandon my friends.",
        "The sins were framed, not broken.",
        "True strength comes from purpose."
    ],

    "LoK": [
        "Balance must be restored.",
        "The Avatar brings peace.",
        "Change is the only constant.",
        "I won’t run from my destiny.",
        "The spirits guide us.",
        "Unity is the path forward."
    ],

    "LC & OD": [
        "Our choices become our legacy.",
        "Every step forward has a cost.",
        "We survive together or not at all.",
        "The world is shaped by those who act.",
        "Stand firm in chaos.",
        "Hope is forged in conflict."
    ],

    "Re Zero": [
        "I will save you, no matter how many times I die.",
        "From zero, I’ll start again.",
        "Suffering makes us stronger.",
        "I refuse to give up.",
        "If I cannot win, I’ll try again.",
        "This time… I’ll get it right."
    ],

    "Ragnarok": [
        "The gods will fall.",
        "Fate cannot bind me.",
        "War chooses no sides.",
        "Strength decides destiny.",
        "Stand proud even in death.",
        "The end begins with one strike."
    ],

    "Daybreak": [
        "I make my own rules now.",
        "The apocalypse is my playground.",
        "Survival has no guidebook.",
        "We’re the last kids on Earth.",
        "Chaos feels like home now.",
        "Find your tribe — or die alone."
    ],

    "Locke and Key": [
        "Every key unlocks something new.",
        "Magic has a cost.",
        "The past never stays buried.",
        "The keys choose their holders.",
        "Fear is the strongest lock.",
        "The house remembers everything."
    ],

    "Code Geass Lelouch of the Rebellion": [
        "I, Lelouch, command you.",
        "The only ones who should kill are those prepared to be killed.",
        "The world lies in lies and power.",
        "A rebellion begins with a single step.",
        "If the king doesn’t move, his subjects won’t follow.",
        "I will destroy and recreate the world."
    ],

    "SAO 2": [
        "The bullets decide everything.",
        "Fear keeps you alive.",
        "I will not let you die.",
        "A hero never stops moving forward.",
        "Winning means living.",
        "Strength is surviving the pain."
    ],

    "SAO Alicization": [
        "My soul will be the blade.",
        "I will protect Eugeo’s honor.",
        "A knight stands by his convictions.",
        "The human heart is stronger than any code.",
        "This world is not just a simulation.",
        "We write our own fate."
    ],

    "GGO": [
        "One shot is all it takes.",
        "Stay low, shoot high.",
        "The battlefield doesn’t forgive mistakes.",
        "Fear sharpens the senses.",
        "I fight to survive.",
        "Victory favors the prepared."
    ],

    "Devilman Crybaby": [
        "A world without love is doomed.",
        "Humans and demons aren’t so different.",
        "If I can’t save you, I’ll cry for you.",
        "The world will drown in its sorrow.",
        "Love is the only thing worth fighting for.",
        "Cry for those you couldn’t save."
    ],

    "Star Trek Lower Decks": [
        "We keep the ship running.",
        "Not all heroes are on the bridge.",
        "Lower decks, top performance.",
        "We boldly go… eventually.",
        "Chaos is part of the job.",
        "Ensigns unite!"
    ],

    "Erased": [
        "I will rewrite the past.",
        "Trust your instincts.",
        "Courage changes destiny.",
        "The truth hides in time.",
        "Saving one life can save the future.",
        "A step back can be a step forward."
    ],

    "Food Wars": [
        "A dish can change the world!",
        "I’ll take your taste buds to heaven.",
        "Cooking is a battle of creativity.",
        "I cook with passion, not fear!",
        "Let the food war begin!",
        "Every flavor tells a story."
    ],

    "Merlin": [
        "None of us can choose our destiny.",
        "I have magic… and I must use it well.",
        "The future is never clear.",
        "Even the smallest act can change the world.",
        "I serve Arthur, and that is enough.",
        "Our paths are intertwined."
    ],

    "Disenchanted": [
        "Magic doesn’t solve everything.",
        "This kingdom is a mess… again.",
        "Chaos is my comfort zone.",
        "Destiny is overrated.",
        "I break curses for breakfast.",
        "Sarcasm is my strongest spell."
    ],

    "Blue Exorcist": [
        "My flames won’t control me.",
        "I’ll become the Paladin.",
        "I’m not afraid of my fate anymore.",
        "A demon can choose to be human.",
        "I’ll make my own path.",
        "I won’t run away again."
    ],

    "Death Note": [
        "I am justice.",
        "The human whose name is written shall die.",
        "This world is rotten.",
        "I will become the god of this new world.",
        "A genius solves a puzzle. A criminal uses it.",
        "You can’t win against someone willing to lose it all."
    ],

    "TDI": [
        "I’m in it to win it!",
        "Drama is my middle name.",
        "Trust no one on this island.",
        "The challenge is everything.",
        "All’s fair in love and competition.",
        "The show must go on!"
    ],

    "Durarara": [
        "The city is alive.",
        "Everyone has a secret.",
        "Chaos is Ikebukuro’s heartbeat.",
        "The headless rider watches all.",
        "Connections shape the world.",
        "Not every monster hides in the dark."
    ],

    "Durarara 2": [
        "The story continues in the shadows.",
        "Ikebukuro never sleeps.",
        "Every thread leads somewhere.",
        "The darkness reveals truth.",
        "Not all friendships last forever.",
        "The city chooses its own destiny."
    ],

    "K": [
        "Kings are born, not made.",
        "A king protects his clan.",
        "Power must be controlled.",
        "Every color has meaning.",
        "Balance keeps the world alive.",
        "The burden of the crown is heavy."
    ],

    "K The Lost King": [
        "The sword chooses its wielder.",
        "Every king carries a sin.",
        "The future rests on lost truths.",
        "Even a fallen king leaves a legacy.",
        "The clans must survive.",
        "Light shines brightest in loss."
    ],

    "Kakegura": [
        "Risk is the ultimate thrill.",
        "I live for the gamble.",
        "Your move decides your fate.",
        "Nothing is sweeter than victory.",
        "Fear clouds judgment.",
        "The house always wins — unless I’m playing."
    ],

    "Sakaki K": [
        "Power flows where purpose goes.",
        "Strength is found in stillness.",
        "The world bends to the focused mind.",
        "Only truth cuts through chaos.",
        "Resolve shapes destiny.",
        "A warrior’s heart never wavers."
    ],

    "Darwin’s Game": [
        "This is more than a game.",
        "I’ll survive no matter what.",
        "Every decision is life or death.",
        "Trust is a luxury.",
        "You grow stronger or die trying.",
        "Adapt to win."
    ],

    "Sherlock Holmes": [
        "The game is on.",
        "You see, but you do not observe.",
        "Data, data, data!",
        "My mind rebels at stagnation.",
        "Once you eliminate the impossible…",
        "The truth always reveals itself."
    ],

    "JL Action": [
        "Justice never takes a day off.",
        "Heroes act, villains react.",
        "We fight as one.",
        "Every mission counts.",
        "Courage under pressure.",
        "Action is our specialty."
    ],

    "JL War": [
        "We fight as one.",
        "The world needs the Justice League.",
        "Stand together or fall alone.",
        "The war is just beginning.",
        "Heroes aren’t born — they rise.",
        "Earth will not fall today."
    ],

    "JL Unlimited": [
        "Justice is never done.",
        "A better world starts with us.",
        "United, we are unstoppable.",
        "We always get back up.",
        "A hero isn’t the suit — it’s the choice.",
        "Courage doesn’t require powers."
    ],

    "So I’m a Spider So What": [
        "I’m just a spider, okay?",
        "Survive now, panic later.",
        "Skill acquired!",
        "This world wants me dead.",
        "I refuse to be eaten.",
        "I’ll crawl my way to the top!"
    ],

    "That Time I Reincarnated as a Slime": [
        "I’m Rimuru Tempest.",
        "Let’s build a nation where everyone belongs.",
        "Strength comes from unity.",
        "I will protect my people.",
        "This world is full of potential.",
        "A slime can change destiny."
    ],

    "Rick and Morty": [
        "Wubba lubba dub dub!",
        "Get schwifty!",
        "Nobody exists on purpose.",
        "Don’t think about it.",
        "What, so everyone’s supposed to sleep every night now?",
        "Sometimes science is more art than science."
    ],

    "Generator Rex": [
        "I’m not a weapon.",
        "I’m Rex, and I fix things.",
        "The world needs a cure.",
        "I control my own powers.",
        "Time to evo up.",
        "Nothing can break my will."
    ],

    "Arcane": [
        "We shared a vision.",
        "We were sisters once.",
        "Progress comes at a price.",
        "Power changes everything.",
        "Everyone wants to be heard.",
        "The world doesn’t give you anything — you take it."
    ],

    "Jobless Reincarnation": [
        "This time, I’ll live with purpose.",
        "A second life deserves effort.",
        "I refuse to waste this chance.",
        "Strength comes from struggle.",
        "Magic is a path to redemption.",
        "The past doesn’t define my future."
    ],

    "Steven Universe": [
        "Believe in Steven.",
        "If every porkchop were perfect…",
        "We are the Crystal Gems!",
        "Change is never easy.",
        "You have to forgive yourself.",
        "Everyone has something precious to protect."
    ],

    "SU Future": [
        "Healing takes time.",
        "I need to understand myself.",
        "I’m allowed to grow.",
        "Not every story ends neatly.",
        "My past doesn’t chain me.",
        "Moving forward is scary, but worth it."
    ],

    "SU The Movie": [
        "Happily ever after takes work.",
        "We can change together.",
        "No one is unfixable.",
        "You can always choose who you become.",
        "Love brings us back.",
        "Growth never ends."
    ],

    "Justice League Animated": [
        "We stand together as one.",
        "Justice will prevail.",
        "Heroes push forward.",
        "Strength lies in unity.",
        "The League protects all.",
        "We don’t run from danger."
    ],

    "Batman Ninja": [
        "A ninja is always prepared.",
        "Gotham follows me, even in time.",
        "Honor guides the blade.",
        "The shadows are my ally.",
        "I will restore order.",
        "The Dark Knight adapts."
    ],

    "Batman vs Robin": [
        "Blood is not destiny.",
        "Family can break or build you.",
        "Justice before vengeance.",
        "I will not lose my son.",
        "A Robin must choose his path.",
        "Control your anger — or it controls you."
    ],

    "Batman Year One": [
        "Fear is a tool.",
        "The city needs a symbol.",
        "I must become more.",
        "Justice starts small.",
        "Gotham's criminals will learn fear.",
        "This is the beginning of the legend."
    ],

    "Batman The Long Halloween": [
        "Every night has a pattern.",
        "Fear the calendar.",
        "Gotham hides its darkest sins.",
        "Justice requires patience.",
        "Everyone has secrets.",
        "Holidays bring out monsters."
    ],

    "Titans": [
        "We’re stronger together.",
        "You can’t outrun your past.",
        "Heroes aren’t born perfect.",
        "Darkness is part of who we are.",
        "I choose my own path.",
        "Titans forever."
    ],

    "Green Lantern First Flight": [
        "In brightest day, in blackest night.",
        "I feel the power of the ring.",
        "Fear is the enemy.",
        "Willpower conquers all.",
        "The Corps stands united.",
        "Light over darkness."
    ],

    "Judas Contract": [
        "Trust is earned, not given.",
        "Betrayal cuts deepest.",
        "We won’t fall apart.",
        "Heroes forgive — but never forget.",
        "Strength is built through trials.",
        "We protect our own."
    ],

    "Public Enemies Superman and Batman": [
        "We fight for what’s right.",
        "Truth and justice will prevail.",
        "You can't control fear — you face it.",
        "Two heroes, one mission.",
        "Evil fears unity.",
        "We’re stronger as a team."
    ],

    "Batman and Harley Quinn": [
        "Justice needs a little chaos.",
        "I work better alone… usually.",
        "You never know what Harley will do next.",
        "Good and bad aren’t always black and white.",
        "Sometimes saving the world gets messy.",
        "We make an unlikely team."
    ],

    "Flashpoint Paradox": [
        "One choice can change everything.",
        "The timeline is broken.",
        "You can’t outrun fate.",
        "Heroes rise in any world.",
        "The world isn’t supposed to be like this.",
        "Fix the past, save the future."
    ],

    "Adventure Time": [
        "What time is it?",
        "Mathematical!",
        "Everything small is just a smaller version of something big.",
        "Sucking at something is the first step to being sorta good at something.",
        "Homies help homies.",
        "Dude, suckin’ at something is the first step to being sorta good at something.",
        "Nobody exists on purpose Nobody belongs anywhere Everybody's gonna die.",
        "When everything is falling apart, that's when things are about to be put back together."
    ],

    "STAS": [
        "Truth and justice always prevail.",
        "I stand for hope.",
        "Superman never backs down.",
        "The world needs someone to believe in.",
        "Strength is nothing without compassion.",
        "Metropolis deserves better."
    ],

    "Adventure Time Distant Lands": [
        "The journey never really ends.",
        "We all grow differently.",
        "Sometimes finding yourself takes time.",
        "Adventure is where you make it.",
        "Friends help you find your way.",
        "Change is part of the adventure."
    ],

    "Leverage Reboot": [
        "Sometimes bad guys make the best good guys.",
        "You’re not alone — we’ve got your back.",
        "We provide… leverage.",
        "Every con has a purpose.",
        "Justice can be creative.",
        "Let’s go steal a win."
    ],

    "OK KO": [
        "Be the hero you know you can be!",
        "Let’s be heroes!",
        "Believe in your own power!",
        "You’re stronger than you think!",
        "Every day is training day!",
        "The plaza needs heroes!"
    ],

    "YuGiOh Zexal": [
        "Kattobingu!",
        "Feel the flow!",
        "You and I will build the ultimate deck!",
        "Dueling is about heart!",
        "My soul blazes with spirit!",
        "High five the sky!"
    ],

    "Invincible": [
        "You need to decide what kind of hero you want to be.",
        "Think, Mark!",
        "You’re stronger than you know.",
        "This world needs protecting.",
        "Being a hero means sacrifice.",
        "The truth can hurt more than any punch.",
        "I am invincible"
    ],

    "Problem Children Are Coming from Another World": [
        "Strength comes from confidence.",
        "Games decide everything here.",
        "I never back down.",
        "This world runs on challenges.",
        "Winning is just the beginning.",
        "Let’s rewrite the rules."
    ],

    "Eden Zero": [
        "The universe is our playground.",
        "Friendship is the real power.",
        "Every adventure starts with a step.",
        "Machines have hearts too.",
        "I won’t abandon my friends.",
        "The stars guide our journey."
    ],

    "Lab Rats": [
        "We’re a team — glitches and all.",
        "Bionics aren’t a curse; they’re a gift.",
        "Heroes support each other.",
        "Failure isn’t the end, it’s training.",
        "We can handle anything together.",
        "Stronger as a family."
    ],

    "Amazing World of Gumball": [
        "This is totally normal… right?",
        "Chaos is just Tuesday.",
        "Why is life like this?",
        "Let’s make this weird.",
        "Everything is ridiculous and I love it.",
        "Normal is overrated."
    ],

    "Static Shock": [
        "I am Static Shock!",
        "Electricity is my superpower.",
        "I fight for the city.",
        "Power with purpose.",
        "Shocking, isn’t it?",
        "Heroes rise where they’re needed.",
        "The world changes and grows, and he's blind to it! Ignorant! And proud of that, too!"
    ],

    "BTAS": [
        "I am vengeance. I am the night.",
        "Justice never sleeps.",
        "Criminals are a cowardly lot.",
        "The shadows protect the innocent.",
        "Fear is my ally.",
        "Gotham is my responsibility."
    ],

    "The New Adventures of Batman": [
        "Gotham will always need Batman.",
        "Justice takes patience.",
        "My mission never ends.",
        "Fear brings out the truth.",
        "I protect those who can’t protect themselves.",
        "The night is my ally."
    ],

    "Vixen": [
        "The animal kingdom is my power.",
        "Strength comes from within.",
        "I honor the spirits of nature.",
        "The world needs balance.",
        "I run with the power of beasts.",
        "Courage is my compass."
    ],

    "The Death of Superman": [
        "Metropolis must be saved.",
        "Hope never dies.",
        "I will stand my ground.",
        "A hero gives everything.",
        "The world needs Superman.",
        "Courage defines sacrifice."
    ],

    "Reign of the Supermen": [
        "The world must decide its heroes.",
        "A symbol can’t be replaced.",
        "Every hero carries a legacy.",
        "Truth unites us.",
        "The future needs belief.",
        "Superman lives on in us."
    ],

    "GTAS": [
        "The city never sleeps.",
        "Justice flies fast.",
        "Every villain gets caught eventually.",
        "Truth moves faster than lies.",
        "I protect everyone — always.",
        "Speed defines the hero."
    ],

    "TMNT Half Shell": [
        "Heroes in a half shell!",
        "Turtle power!",
        "We fight as brothers.",
        "Cowabunga!",
        "Ninjas never quit.",
        "Honor is our way."
    ],

    "Dark Knight Trilogy": [
        "Why do we fall? So we can learn to pick ourselves up.",
        "It's not who I am underneath… but what I do that defines me.",
        "Some men just want to watch the world burn.",
        "A hero can be anyone.",
        "The night is darkest before the dawn.",
        "Madness is like gravity — all it takes is a little push."
    ],

    "The Batman 2022": [
        "I am vengeance.",
        "Fear is a tool.",
        "I can't be everywhere, but I can be enough.",
        "The city needs hope, not just vengeance.",
        "Justice can be cruel.",
        "The real mask is who we choose to be."
    ],

    "Spider-Man OG Trilogy": [
        "With great power comes great responsibility.",
        "Go get 'em, tiger.",
        "I missed the part where that's my problem.",
        "It's a choice — the choice to be a hero.",
        "You mess with one of us, you mess with all of us!",
        "Being Spider-Man comes at a price."
    ],

    "Amazing Spider-Man Live Action": [
        "You have to take responsibility for your gifts.",
        "I made promises I couldn't keep.",
        "Secrets have a cost.",
        "I’m trying to be better than I was.",
        "This city needs someone to watch over it.",
        "The mask is what gives me strength."
    ],

    "Spider-Man Home Trilogy": [
        "I just wanted to be like you, Mr. Stark.",
        "If you’re nothing without the suit, then you shouldn’t have it.",
        "I can do this all day… no wait, wrong guy.",
        "The world needs friendly neighborhood heroes.",
        "Don’t do anything I would do… or wouldn’t do.",
        "Responsibility means growing up."
    ],

    "ASMTAS": [
        "Responsibility is the heart of a hero.",
        "Everyone deserves a second chance.",
        "The city needs protecting.",
        "Mask or no mask, I choose to help.",
        "Courage means standing alone sometimes.",
        "Heroes rise through hardship."
    ],

    "IMTAS": [
        "I fight for what’s right.",
        "Never underestimate a good heart.",
        "The world counts on me.",
        "Strength comes from the will to change.",
        "Every villain fears the truth.",
        "Light shines brightest through darkness."
    ],

    "Inside Job": [
        "The world is a conspiracy — literally.",
        "I run this shadow government like a pro.",
        "Everything is connected… unfortunately.",
        "Trust no one, especially your coworkers.",
        "This job is a nightmare I can’t quit.",
        "Paranoia is just pattern recognition."
    ],

    "Johnny Test": [
        "This is gonna be awesome!",
        "Adventure is my middle name!",
        "I never back down!",
        "Let’s crank this up!",
        "Science makes everything cooler!",
        "Johnny Test always finds a way!"
    ],

    "Spider-Man Animated Series": [
        "My spider-sense is tingling.",
        "Power comes with responsibility.",
        "I won’t let the city fall.",
        "A hero stands even when the world falls apart.",
        "Courage web-slings through fear.",
        "Every choice shapes the hero I become."
    ],

    "Ultimate Spider-Man": [
        "I’m the ultimate Spider-Man!",
        "Teamwork makes us stronger.",
        "S.H.I.E.L.D. always has another mission.",
        "A hero learns from failure.",
        "Let’s swing into action!",
        "Being a hero is messy, but worth it."
    ],

    "The Owl House": [
        "Us weirdos have to stick together.",
        "I choose to be my own witch.",
        "Magic is about expressing yourself.",
        "The world is full of strange wonders.",
        "I won’t let fear decide my fate.",
        "Growth is messy — and magical."
    ],

    "Brooklyn 99": [
        "Cool cool cool cool cool.",
        "No doubt, no doubt.",
        "Nine-Nine!",
        "Title of your sex tape.",
        "Believe in yourself — and your precinct.",
        "I’m ready to make justice my bitch."
    ],

    "Amphibia": [
        "I’m not the girl I used to be.",
        "The journey changes us.",
        "Friendship can save worlds.",
        "Courage comes from the heart.",
        "The future isn’t written — we write it.",
        "Even frogs need heroes.",
        "I gave you this, I gave you everything!"
    ],

    "Infinity Train": [
        "Every number means something.",
        "You must face your past.",
        "The train helps you grow… painfully.",
        "Your choices define your car.",
        "Nothing changes unless you do.",
        "Growth starts with understanding."
    ],

    "Gortimer Gibbons Life on Normal Street": [
        "Normal is stranger than you think.",
        "Every street has magic.",
        "Friendship gets you through anything.",
        "Mystery lives in the everyday.",
        "Growing up is an adventure.",
        "Believe in the weirdness around you.",
        "No one is afraid of the dark - they're afraid of what the dark hides",
        "They say love is blind, but the real danger is being blind to love.",
        "I guess the trick is figuring out how much light you need to make yourself happy."
    ],

    "Fantastic Four World’s Greatest Heroes": [
        "Flame on!",
        "It’s clobberin’ time!",
        "We protect the world — together.",
        "Family is our real superpower.",
        "Science and bravery go hand in hand.",
        "The world needs the Fantastic Four."
    ],

    "Milo Murphy’s Law": [
        "Anything that can go wrong will go wrong.",
        "We’ll handle whatever comes our way.",
        "Preparedness is my superpower.",
        "Stay positive — chaos is inevitable.",
        "Embrace the unexpected.",
        "Murphy’s Law is just another challenge."
    ],

    "Phineas and Ferb": [
        "Ferb, I know what we’re gonna do today.",
        "Aren’t you a little young for this?",
        "Yes, yes I am.",
        "Where’s Perry?",
        "We’re making the most of every day!",
        "The possibilities are endless."
    ],

    "Wizards of Waverly Place": [
        "Everything is not what it seems.",
        "Magic has consequences.",
        "A wizard must earn their title.",
        "Family and magic don’t always mix.",
        "The Russo way is… complicated.",
        "You can choose who you become."
    ],

    "Kickin’ It": [
        "We fight as a team.",
        "Wasabi warriors never quit!",
        "Believe in yourself.",
        "Strength is earned, not given.",
        "Courage kicks fear in the face.",
        "Every warrior has a path."
    ],

    "The Mandalorian": [
        "This is the way.",
        "I can bring you in warm… or cold.",
        "Wherever I go, he goes.",
        "I walk the path of the Mand’alor.",
        "Honor is my guide.",
        "A Mandalorian is stronger with allies."
    ],

    "Krypton": [
        "The future of the House of El begins here.",
        "A hero’s legacy is forged long before the hero.",
        "Krypton’s fate is mine to challenge.",
        "We cannot let destiny decide for us.",
        "Hope must not die here.",
        "The past shapes us, but does not define us."
    ],

    "Kaijudo": [
        "Only those with heart can command the creatures.",
        "The duel is a bond, not a battle.",
        "Courage calls the strongest allies.",
        "The Veil protects our world.",
        "Trust in your creature partners.",
        "Every summon comes with responsibility."
    ],

    "Magi Nation": [
        "The dream realm chooses its champions.",
        "Magic lies within those who seek it.",
        "Every creature has a bond with its caller.",
        "Courage lights the path forward.",
        "The realms depend on our choices.",
        "Only heart can tame true power."
    ],

    "Blue Period": [
        "Art is a battle with yourself.",
        "Find the beauty only you can see.",
        "Passion is worth the struggle.",
        "Creation comes from pain and joy.",
        "Art changes the artist first.",
        "You must paint your own truth."
    ],

    "My Adventures With Superman": [
        "I just want to help people.",
        "Being Superman doesn’t mean being alone.",
        "Hope can inspire anyone.",
        "A hero is someone who chooses kindness.",
        "The world needs more than strength — it needs heart.",
        "I won’t give up on anyone."
    ],

    "Adventure Time Fionna and Cake": [
        "Our story is ours to write.",
        "Magic or no magic, we choose our destiny.",
        "Being ordinary doesn’t make you less.",
        "You can still be a hero in your own way.",
        "The multiverse is full of surprises.",
        "Every version of us matters."
    ],

    "Red vs Blue": [
        "You ever wonder why we’re here?",
        "Bow chicka bow wow.",
        "That’s the stupidest idea I’ve ever heard — let’s do it.",
        "War is just diplomacy with bullets.",
        "Chaos is a lifestyle.",
        "We fight because… we fight."
    ],

    "TMNT Mutant Mayhem": [
        "Turtles unite!",
        "We’re stronger together.",
        "Mutants are family.",
        "Being different is our greatest strength.",
        "We protect our city — even when it fears us.",
        "Heroes come in all shapes and shells."
    ],

    "Star Trek Prodigy": [
        "We’re more than runaways — we’re a crew.",
        "Hope is the first step toward discovery.",
        "The stars belong to everyone.",
        "A captain leads with heart.",
        "Every journey begins with trust.",
        "We choose who we become."
    ],

    "Jentry Chao vs the Underworld": [
        "Monsters don’t scare me — failure does.",
        "Magic comes from belief.",
        "Courage starts small.",
        "Even heroes have messy beginnings.",
        "Face your demons — literally.",
        "The underworld can’t stop determination."
    ],

    "Dead End Paranormal Park": [
        "Your demons can become your strength.",
        "Friendship conquers everything — even hell.",
        "Bravery is doing things scared.",
        "Magic comes from believing in yourself.",
        "Together, we’re unstoppable.",
        "Even the spooky stuff deserves compassion."
    ],

    "A Silent Voice": [
        "I want to make things right.",
        "Can we start over?",
        "Redemption begins with a single step.",
        "I’m listening — really listening.",
        "Silence can hurt deeper than words.",
        "Everyone deserves a second chance."
    ],

    "Black Clover": [
        "I’ll become the Wizard King!",
        "My magic is never giving up.",
        "Surpass your limits — right now!",
        "A grimoire chooses its mage.",
        "Strength is forged through hardship.",
        "Together, we surpass limits."
    ],

    "Chainsaw Man": [
        "I just want a normal life.",
        "If I get to touch some boobs, I’ll fight.",
        "Devils fear those who are insane enough.",
        "The world is cruel — fight anyway.",
        "Blood, blades, and survival.",
        "I refuse to die until I taste happiness."
    ],

    "Solo Leveling": [
        "I alone level up.",
        "From weakest hunter to strongest.",
        "Arise.",
        "Power answers to me now.",
        "I will surpass every limit.",
        "Fear me — or follow me."
    ],

    "Gumball Chronicles": [
        "This is the stupidest amazing idea ever.",
        "Chaos is our specialty.",
        "Reality bends around our nonsense.",
        "Why is everything like this?",
        "Let’s make today weird.",
        "Logic is optional."
    ],

    "Haunted Hotel": [
        "Every room has a story — and a ghost.",
        "The spirits never left.",
        "Fear lives here.",
        "Some doors should never be opened.",
        "History haunts us all.",
        "The hotel remembers everyone."
    ],

}


# In[15]:


def clean_quote(quote: str) -> str:
    # Remove punctuation
    translator = str.maketrans('', '', string.punctuation)
    quote = quote.translate(translator)

    # Remove spaces
    quote = quote.replace(" ", "")

    # Lowercase everything
    quote = quote.lower()

    # Capitalize ONLY the first letter
    if len(quote) > 0:
        quote = quote[0].upper() + quote[1:]

    return quote


# In[16]:


def generate_password(show=None):
    # If no show is chosen, pick a random show
    if show is None:
        show = secrets.choice(list(SHOW_QUOTES.keys()))

    # Pick a random quote from that show
    quote = secrets.choice(SHOW_QUOTES[show])

    # Clean it
    cleaned = clean_quote(quote)

    # Add required ending
    password = cleaned + "2!"

    return password

def generate_multiple(n=10, show=None):
    return [generate_password(show) for _ in range(n)]


if __name__ == "__main__":
    print("Random password:", generate_password())
    show = input("Enter a show name (or leave blank for random): ").strip()

    if show == "":
        print("Generated:", generate_password())
    else:
        if show not in SHOW_QUOTES:
            print("Show not found!")
        else:
            print("Generated:", generate_password(show))
    
    input("\nPress ENTER to exit.")
