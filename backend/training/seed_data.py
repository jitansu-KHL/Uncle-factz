"""
Domain-labeled seed examples used to train each specialist classifier.

Each row: claim, evidence, verdict.
Evidence mimics retrieved web snippets so the model learns claim+context,
not claim-only memorization.
"""

SCIENCE = [
    {
        "claim": "Water boils at 100 degrees Celsius at standard atmospheric pressure.",
        "evidence": "At 1 atmosphere (101.325 kPa), pure water boils at 100 °C. Boiling point decreases at higher altitudes.",
        "verdict": "True",
    },
    {
        "claim": "The Earth is a flat disc.",
        "evidence": "Geodesy, satellite imagery, and circumnavigation show Earth is an oblate spheroid, not a disc.",
        "verdict": "False",
    },
    {
        "claim": "The speed of light in vacuum is approximately 299,792 kilometers per second.",
        "evidence": "The defined speed of light in vacuum is exactly 299,792,458 m/s (about 299,792 km/s).",
        "verdict": "True",
    },
    {
        "claim": "Humans and dinosaurs lived at the same time.",
        "evidence": "Non-avian dinosaurs went extinct about 66 million years ago. Anatomically modern humans appeared roughly 300,000 years ago.",
        "verdict": "False",
    },
    {
        "claim": "The James Webb Space Telescope detected carbon-bearing molecules in the atmosphere of exoplanet K2-18b.",
        "evidence": "NASA reported JWST observations of K2-18b consistent with methane and carbon dioxide in its atmosphere.",
        "verdict": "True",
    },
    {
        "claim": "Lightning never strikes the same place twice.",
        "evidence": "Lightning frequently strikes tall structures repeatedly. The Empire State Building is struck dozens of times per year.",
        "verdict": "False",
    },
    {
        "claim": "DNA is a double helix.",
        "evidence": "Watson and Crick described DNA as a double helix; later crystallography confirmed the structure.",
        "verdict": "True",
    },
    {
        "claim": "The Sun orbits the Earth.",
        "evidence": "Heliocentric models and orbital mechanics show Earth and other planets orbit the Sun.",
        "verdict": "False",
    },
    {
        "claim": "There are eight recognized planets in the Solar System.",
        "evidence": "After the 2006 IAU definition, Pluto is a dwarf planet, leaving eight planets.",
        "verdict": "True",
    },
    {
        "claim": "Global average temperatures have risen since the late 19th century.",
        "evidence": "NASA GISS and NOAA records show roughly 1.1 °C of warming since 1880, with recent decades the warmest.",
        "verdict": "True",
    },
    {
        "claim": "A perpetual motion machine that produces unlimited energy with no input has been demonstrated in a peer-reviewed lab.",
        "evidence": "Perpetual motion of this type would violate conservation of energy. No verified laboratory demonstration exists.",
        "verdict": "False",
    },
    {
        "claim": "Antibiotics kill viruses.",
        "evidence": "Antibiotics target bacteria. Viruses lack the cellular machinery antibiotics act on.",
        "verdict": "False",
    },
    {
        "claim": "Evolution by natural selection is supported by multiple independent lines of evidence.",
        "evidence": "Fossil records, comparative anatomy, genetics, and observed speciation support evolutionary theory.",
        "verdict": "True",
    },
    {
        "claim": "The Great Wall of China is visible from the Moon with the naked eye.",
        "evidence": "NASA states the Great Wall is not visible from the Moon unaided. Even from low Earth orbit it is difficult to see.",
        "verdict": "False",
    },
    {
        "claim": "Atoms are mostly empty space.",
        "evidence": "Atomic nuclei occupy a tiny fraction of atomic volume; most of an atom is electron cloud / empty space.",
        "verdict": "True",
    },
    {
        "claim": "Sound travels faster in air than in steel.",
        "evidence": "Sound speed in steel is several kilometers per second, far faster than ~343 m/s in air at 20 °C.",
        "verdict": "False",
    },
    {
        "claim": "Photosynthesis converts light energy into chemical energy stored in sugars.",
        "evidence": "Chloroplasts use light to fix CO2 into carbohydrates; this is the core of photosynthesis.",
        "verdict": "True",
    },
    {
        "claim": "The Moon produces its own visible light like a star.",
        "evidence": "The Moon shines by reflecting sunlight; it is not a self-luminous star.",
        "verdict": "False",
    },
    {
        "claim": "Some exoplanets have been detected using the transit method.",
        "evidence": "Kepler and TESS discovered thousands of exoplanets via periodic dips in stellar brightness.",
        "verdict": "Mostly True",
    },
    {
        "claim": "All dinosaurs were cold-blooded reptiles identical to modern lizards.",
        "evidence": "Many dinosaurs show evidence of elevated metabolism; birds are living dinosaurs. The claim oversimplifies.",
        "verdict": "False",
    },
    {
        "claim": "Water can exist as solid, liquid, and gas on Earth.",
        "evidence": "Ice, liquid water, and water vapor are common phases under terrestrial conditions.",
        "verdict": "True",
    },
    {
        "claim": "A newly discovered mineral on Mars proves there was never any water on the planet.",
        "evidence": "Mars shows extensive evidence of past liquid water (valley networks, hydrated minerals). A single mineral find would not erase that record.",
        "verdict": "False",
    },
    {
        "claim": "Neutrinos interact only weakly with matter.",
        "evidence": "Neutrinos interact via the weak force (and gravity), so they pass through large amounts of matter with low probability of interaction.",
        "verdict": "True",
    },
    {
        "claim": "Scientists have measured the exact number of alien civilizations in the Milky Way.",
        "evidence": "No confirmed census of extraterrestrial civilizations exists. Drake-equation estimates are highly uncertain.",
        "verdict": "Insufficient Evidence",
    },
    {
        "claim": "Dark matter has been directly detected in a laboratory and fully identified as a specific particle.",
        "evidence": "Dark matter is inferred from gravitational effects. Direct detection experiments have not conclusively identified a particle.",
        "verdict": "False",
    },
    {
        "claim": "CRISPR-Cas9 can be used to edit DNA sequences.",
        "evidence": "CRISPR-Cas9 is a widely used genome-editing tool that cuts DNA at targeted sites.",
        "verdict": "True",
    },
    {
        "claim": "The ozone hole over Antarctica has been linked to chlorofluorocarbons.",
        "evidence": "CFCs deplete stratospheric ozone; the Montreal Protocol reduced CFCs and the Antarctic ozone hole has shown recovery signs.",
        "verdict": "True",
    },
    {
        "claim": "Earth's magnetic field is generated entirely by permanent magnets in the crust.",
        "evidence": "The geomagnetic field is primarily generated by dynamo action in the liquid outer core, not crustal permanent magnets.",
        "verdict": "False",
    },
    {
        "claim": "A 2026 preprint claims a room-temperature superconductor but independent labs have not yet replicated it.",
        "evidence": "No independent replication is cited. Extraordinary materials claims require confirmation.",
        "verdict": "Insufficient Evidence",
    },
    {
        "claim": "Black holes exist and have been observed indirectly and via imaging.",
        "evidence": "Stellar orbits near Sgr A*, gravitational waves from mergers, and EHT images of M87* and Sgr A* support black holes.",
        "verdict": "True",
    },
    {
        "claim": "All scientific theories are just guesses with no predictive power.",
        "evidence": "Scientific theories are tested explanatory frameworks; many make precise, repeatedly confirmed predictions.",
        "verdict": "False",
    },
    {
        "claim": "Venus is hotter than Mercury despite being farther from the Sun.",
        "evidence": "Venus has a dense CO2 atmosphere and greenhouse effect; surface temperatures exceed Mercury's.",
        "verdict": "True",
    },
    {
        "claim": "Quantum computers have fully replaced classical supercomputers for all tasks.",
        "evidence": "Quantum devices are experimental and excel at limited problem classes; they have not replaced general-purpose supercomputers.",
        "verdict": "False",
    },
    {
        "claim": "Seafloor spreading supports plate tectonics.",
        "evidence": "Magnetic striping and age progression of oceanic crust are classic evidence for seafloor spreading.",
        "verdict": "True",
    },
    {
        "claim": "A viral post says a new particle was discovered last night at CERN but no paper or CERN bulletin is available.",
        "evidence": "No official CERN announcement or peer-reviewed paper is provided for the alleged discovery.",
        "verdict": "Insufficient Evidence",
    },
    {
        "claim": "Helium is a noble gas and is chemically largely inert under ordinary conditions.",
        "evidence": "Helium has a filled 1s shell and forms compounds only under extreme conditions.",
        "verdict": "True",
    },
    {
        "claim": "The observable universe is about 13.8 billion years old.",
        "evidence": "Planck and other cosmological measurements put the age of the universe at about 13.8 billion years.",
        "verdict": "True",
    },
    {
        "claim": "Glass at room temperature is a rapidly flowing liquid that visibly sags in old windows over years.",
        "evidence": "Window-glass sagging is a myth; apparent thickness variation is from historic manufacturing. Glass is an amorphous solid.",
        "verdict": "False",
    },
    {
        "claim": "Some birds are living dinosaurs.",
        "evidence": "Phylogenetic classification places birds within theropod dinosaurs.",
        "verdict": "True",
    },
    {
        "claim": "A private blog claims Earth's core is made of ice.",
        "evidence": "Seismology indicates a solid inner core and liquid outer core composed mainly of iron and nickel.",
        "verdict": "False",
    },
]

HEALTH = [
    {
        "claim": "Vaccines cause autism.",
        "evidence": "Large epidemiological studies found no causal link between vaccines and autism. The original Wakefield paper was retracted for fraud.",
        "verdict": "False",
    },
    {
        "claim": "Drinking 5 liters of alkaline water daily completely prevents heart disease.",
        "evidence": "No clinical guideline supports alkaline water as complete prevention of heart disease. Risk reduction involves diet, exercise, not smoking, and medical care.",
        "verdict": "False",
    },
    {
        "claim": "Eating garlic daily cures all viral respiratory infections entirely.",
        "evidence": "Garlic has been studied for modest immune effects but does not cure viral respiratory infections.",
        "verdict": "False",
    },
    {
        "claim": "Handwashing with soap reduces transmission of many infectious diseases.",
        "evidence": "WHO and CDC recommend hand hygiene as a proven way to reduce diarrheal and respiratory infections.",
        "verdict": "True",
    },
    {
        "claim": "Antibiotics are effective against bacterial infections when appropriately prescribed.",
        "evidence": "Antibiotics treat susceptible bacterial infections; stewardship is needed to limit resistance.",
        "verdict": "True",
    },
    {
        "claim": "Smoking tobacco increases the risk of lung cancer.",
        "evidence": "Surgeon General reports and epidemiology show a strong causal link between tobacco smoking and lung cancer.",
        "verdict": "True",
    },
    {
        "claim": "HIV is transmitted by casual hugging.",
        "evidence": "HIV is transmitted via specific body fluids, not casual contact such as hugging or sharing dishes.",
        "verdict": "False",
    },
    {
        "claim": "Insulin is used to treat diabetes mellitus in many patients.",
        "evidence": "Insulin therapy is standard for type 1 diabetes and is used in some people with type 2 diabetes.",
        "verdict": "True",
    },
    {
        "claim": "Sunscreen can help reduce skin damage from ultraviolet radiation.",
        "evidence": "Broad-spectrum sunscreen reduces UV-related skin damage and is recommended by dermatology organizations.",
        "verdict": "True",
    },
    {
        "claim": "Drinking bleach is a safe treatment for COVID-19.",
        "evidence": "Health authorities warn that ingesting bleach is poisonous and is not a COVID-19 treatment.",
        "verdict": "False",
    },
    {
        "claim": "Regular physical activity is associated with lower cardiovascular risk.",
        "evidence": "AHA and WHO guidelines cite physical activity as a major protective factor for heart disease.",
        "verdict": "True",
    },
    {
        "claim": "Humans only use 10% of their brain.",
        "evidence": "Neuroimaging shows widespread brain activity; the 10% myth is false.",
        "verdict": "False",
    },
    {
        "claim": "mRNA COVID-19 vaccines do not alter a person's DNA.",
        "evidence": "mRNA remains in the cytoplasm and is degraded; it does not integrate into the genome under normal vaccination.",
        "verdict": "True",
    },
    {
        "claim": "Homeopathic ultra-dilutions beyond Avogadro's number contain no active molecules of the original substance.",
        "evidence": "Serial dilutions past 12C typically leave no original molecules; effects are not explained by remaining active ingredient.",
        "verdict": "True",
    },
    {
        "claim": "Homeopathy has been proven to cure cancer in large randomized trials accepted as standard of care.",
        "evidence": "Cancer standard of care is not homeopathy. High-quality evidence does not support homeopathy as a cancer cure.",
        "verdict": "False",
    },
    {
        "claim": "Excessive alcohol consumption increases risk of liver disease.",
        "evidence": "Heavy drinking is a major cause of alcoholic liver disease, including cirrhosis.",
        "verdict": "True",
    },
    {
        "claim": "A celebrity tweet says a new herb reverses Alzheimer's in 48 hours.",
        "evidence": "No FDA-approved herb reverses Alzheimer's in 48 hours. Alzheimer's treatments do not work that way.",
        "verdict": "False",
    },
    {
        "claim": "Oral rehydration solution can treat dehydration from diarrhea.",
        "evidence": "WHO recommends ORS as a mainstay of diarrhea dehydration treatment.",
        "verdict": "True",
    },
    {
        "claim": "Vitamin C megadoses prevent all cancers with 100% certainty.",
        "evidence": "Vitamin C is essential but megadoses have not been shown to prevent all cancers.",
        "verdict": "False",
    },
    {
        "claim": "Statins can lower LDL cholesterol in many patients.",
        "evidence": "Clinical trials show statins reduce LDL and cardiovascular events in indicated patients.",
        "verdict": "True",
    },
    {
        "claim": "You should finish a prescribed antibiotic course unless a clinician advises otherwise, and not share leftover antibiotics.",
        "evidence": "Public health guidance discourages leftover/shared antibiotics; duration should follow clinician advice.",
        "verdict": "Mostly True",
    },
    {
        "claim": "Fluoride in community water at recommended levels reduces tooth decay.",
        "evidence": "CDC lists water fluoridation among effective public health measures against dental caries.",
        "verdict": "True",
    },
    {
        "claim": "Sitting too close to a TV permanently ruins children's eyesight in all cases.",
        "evidence": "This is a common myth; near work can cause eye strain but does not universally permanently destroy vision.",
        "verdict": "False",
    },
    {
        "claim": "A small unpublished survey of 12 people claims a smoothie cured hypertension.",
        "evidence": "A 12-person unpublished survey is not adequate evidence that a smoothie cures hypertension.",
        "verdict": "Insufficient Evidence",
    },
    {
        "claim": "Opioid overdose can be reversed by naloxone when given in time.",
        "evidence": "Naloxone is an opioid antagonist used to reverse opioid overdose.",
        "verdict": "True",
    },
    {
        "claim": "Type 2 diabetes is influenced by genetics and lifestyle factors.",
        "evidence": "Risk includes family history, obesity, diet, and physical inactivity.",
        "verdict": "True",
    },
    {
        "claim": "Cracking knuckles has been proven to cause arthritis in every person who does it.",
        "evidence": "Studies have not shown a causal link between knuckle cracking and arthritis.",
        "verdict": "False",
    },
    {
        "claim": "Breastfeeding has health benefits for many infants when it is possible and appropriate.",
        "evidence": "WHO recommends exclusive breastfeeding for 6 months when feasible, with noted health benefits.",
        "verdict": "True",
    },
    {
        "claim": "A TikTok video says hanging upside down detoxes heavy metals from the liver.",
        "evidence": "No medical evidence supports inversion as heavy-metal liver detox. The liver metabolizes toxins via biochemical pathways.",
        "verdict": "False",
    },
    {
        "claim": "HPV vaccination reduces risk of HPV-related cancers.",
        "evidence": "HPV vaccines prevent infection with high-risk types that cause cervical and other cancers.",
        "verdict": "True",
    },
    {
        "claim": "All dietary supplements sold online are FDA-approved drugs.",
        "evidence": "Most supplements are not approved as drugs; FDA does not pre-approve dietary supplements like prescription drugs.",
        "verdict": "False",
    },
    {
        "claim": "Sleep deprivation can impair cognitive performance.",
        "evidence": "Sleep research shows attention, memory, and reaction time decline with insufficient sleep.",
        "verdict": "True",
    },
    {
        "claim": "A clinic's website claims a secret frequency machine diagnosed 40 diseases in one scan; no methods paper is available.",
        "evidence": "No peer-reviewed validation of the device is provided. Extraordinary diagnostic claims need clinical trials.",
        "verdict": "Insufficient Evidence",
    },
    {
        "claim": "Measles is a highly contagious viral disease preventable by vaccination.",
        "evidence": "Measles R0 is high; MMR vaccine is highly effective at preventing measles.",
        "verdict": "True",
    },
    {
        "claim": "Drinking your own urine is a medically recommended treatment for kidney failure.",
        "evidence": "Urine therapy is not a treatment for kidney failure; dialysis or transplant are indicated treatments.",
        "verdict": "False",
    },
    {
        "claim": "Blood pressure control reduces risk of stroke in people with hypertension.",
        "evidence": "Hypertension treatment guidelines are based on trials showing stroke-risk reduction.",
        "verdict": "True",
    },
    {
        "claim": "Placebos can produce perceived symptom changes in some trials, but that does not mean a placebo is a cure for cancer.",
        "evidence": "Placebo effects can influence subjective symptoms; they do not constitute cancer cures.",
        "verdict": "True",
    },
    {
        "claim": "You can catch a cold from being cold itself with no virus involved.",
        "evidence": "Colds are caused by viruses (often rhinoviruses). Cold weather may correlate with transmission but is not the pathogen.",
        "verdict": "False",
    },
    {
        "claim": "A preprint with 8 patients suggests a drug might help a rare disease, but no control group is described.",
        "evidence": "Uncontrolled n=8 preprints are hypothesis-generating, not confirmatory.",
        "verdict": "Insufficient Evidence",
    },
    {
        "claim": "Paracetamol (acetaminophen) overdose can cause severe liver injury.",
        "evidence": "Acetaminophen toxicity is a well-known cause of acute liver failure.",
        "verdict": "True",
    },
]

POLITICS = [
    {
        "claim": "The United Nations was founded in 1945.",
        "evidence": "The UN Charter was signed in 1945 and the organization began operations that year.",
        "verdict": "True",
    },
    {
        "claim": "The United States has a bicameral Congress consisting of the Senate and the House of Representatives.",
        "evidence": "Article I of the U.S. Constitution establishes a Senate and a House of Representatives.",
        "verdict": "True",
    },
    {
        "claim": "The European Union is a single country with one president who is head of state of all member nations.",
        "evidence": "The EU is a union of sovereign member states, not a single country, and members retain their own heads of state.",
        "verdict": "False",
    },
    {
        "claim": "NATO Article 5 states that an armed attack against one member is considered an attack against all.",
        "evidence": "The Washington Treaty Article 5 collective-defense clause is a core NATO commitment.",
        "verdict": "True",
    },
    {
        "claim": "India's parliament is called the Diet.",
        "evidence": "India's national legislature is Parliament (Lok Sabha and Rajya Sabha). The Diet is Japan's legislature.",
        "verdict": "False",
    },
    {
        "claim": "The UK left the European Union following the 2016 referendum, with Brexit taking effect in 2020.",
        "evidence": "The UK voted Leave in 2016 and formally left the EU on 31 January 2020.",
        "verdict": "True",
    },
    {
        "claim": "The World Bank and IMF were created at the Bretton Woods conference in 1944.",
        "evidence": "Bretton Woods established the IMF and the International Bank for Reconstruction and Development (World Bank Group).",
        "verdict": "True",
    },
    {
        "claim": "Permanent members of the UN Security Council have veto power.",
        "evidence": "China, France, Russia, the UK, and the US can veto substantive Security Council resolutions.",
        "verdict": "True",
    },
    {
        "claim": "A social media post says a secret world government passed a law yesterday banning all elections globally.",
        "evidence": "No such global law exists. Elections continue in numerous countries. The claim is unsupported.",
        "verdict": "False",
    },
    {
        "claim": "The US presidential term is four years.",
        "evidence": "The Constitution sets a four-year presidential term.",
        "verdict": "True",
    },
    {
        "claim": "Switzerland is a member of the European Union.",
        "evidence": "Switzerland is not an EU member; it has bilateral agreements with the EU.",
        "verdict": "False",
    },
    {
        "claim": "The Paris Agreement is an international treaty on climate change.",
        "evidence": "The Paris Agreement (2015) is a legally binding international climate treaty under the UNFCCC.",
        "verdict": "True",
    },
    {
        "claim": "GDP is a commonly used measure of a country's economic output.",
        "evidence": "Gross domestic product is a standard national-accounts measure of economic production.",
        "verdict": "True",
    },
    {
        "claim": "Inflation always means that every citizen's wages rose by the exact same percentage.",
        "evidence": "Inflation is a general rise in prices; wages do not automatically rise equally for everyone.",
        "verdict": "False",
    },
    {
        "claim": "The US Bill of Rights comprises the first ten amendments to the Constitution.",
        "evidence": "The Bill of Rights refers to Amendments I–X.",
        "verdict": "True",
    },
    {
        "claim": "A viral claim says a new unnamed bill already confiscated all private property in the United States last week.",
        "evidence": "No enacted federal law confiscated all private property. Property rights remain. The claim is false.",
        "verdict": "False",
    },
    {
        "claim": "The International Court of Justice is the principal judicial organ of the United Nations.",
        "evidence": "The ICJ in The Hague is the UN's principal judicial organ.",
        "verdict": "True",
    },
    {
        "claim": "All countries use the same electoral system of first-past-the-post single-member districts.",
        "evidence": "Electoral systems vary: PR, mixed-member, two-round, FPTP, etc.",
        "verdict": "False",
    },
    {
        "claim": "The WTO deals with the global rules of trade between nations.",
        "evidence": "The World Trade Organization administers trade agreements and dispute settlement among members.",
        "verdict": "True",
    },
    {
        "claim": "A leaked screenshot from an unknown account claims a 50% nationwide price cut is already law, with no bill number.",
        "evidence": "Without a bill number, vote record, or official gazette, the policy claim cannot be verified.",
        "verdict": "Insufficient Evidence",
    },
    {
        "claim": "The African Union is a continental organization of African states.",
        "evidence": "The AU succeeded the OAU and includes most African countries as members.",
        "verdict": "True",
    },
    {
        "claim": "Central banks typically use interest-rate policy among tools to influence inflation.",
        "evidence": "Inflation targeting often involves policy rates, among other instruments.",
        "verdict": "True",
    },
    {
        "claim": "Sanctions automatically collapse any targeted economy within 24 hours in every historical case.",
        "evidence": "Sanctions effects vary widely and do not uniformly collapse economies in a day.",
        "verdict": "False",
    },
    {
        "claim": "The US Senate has 100 senators, two from each state.",
        "evidence": "Each of the 50 states elects two senators.",
        "verdict": "True",
    },
    {
        "claim": "The euro is the official currency of every European country.",
        "evidence": "Not all European countries use the euro (e.g., UK, Switzerland, Sweden, Poland).",
        "verdict": "False",
    },
    {
        "claim": "Freedom of speech protections differ across countries' constitutions and laws.",
        "evidence": "Legal regimes for speech vary substantially by jurisdiction.",
        "verdict": "True",
    },
    {
        "claim": "A campaign flyer claims unemployment fell 90% overnight with no official statistics office release.",
        "evidence": "Labor statistics are published on schedules by statistical agencies. No release supports a 90% overnight drop.",
        "verdict": "Insufficient Evidence",
    },
    {
        "claim": "The Geneva Conventions are treaties setting humanitarian rules in armed conflict.",
        "evidence": "The Geneva Conventions and Additional Protocols are core IHL treaties.",
        "verdict": "True",
    },
    {
        "claim": "Gerrymandering refers to drawing electoral district boundaries to favor a political interest.",
        "evidence": "The term describes partisan or incumbency-favoring district maps.",
        "verdict": "True",
    },
    {
        "claim": "A monarchy and a republic are always identical systems of government.",
        "evidence": "Monarchies have hereditary heads of state; republics typically do not. They are not identical.",
        "verdict": "False",
    },
    {
        "claim": "The OECD is an intergovernmental organization of mostly high-income economies.",
        "evidence": "The Organisation for Economic Co-operation and Development includes many developed economies.",
        "verdict": "True",
    },
    {
        "claim": "Voter ID laws are identical in every democracy worldwide.",
        "evidence": "ID requirements at polls vary widely by country and subnational jurisdiction.",
        "verdict": "False",
    },
    {
        "claim": "The UN General Assembly can pass resolutions; they are not the same as Security Council binding decisions.",
        "evidence": "GA resolutions are generally non-binding recommendations; UNSC decisions under Chapter VII can be binding.",
        "verdict": "Mostly True",
    },
    {
        "claim": "Federal systems divide power between national and subnational governments.",
        "evidence": "Federalism allocates authority across levels, as in the US, India, Germany, and others.",
        "verdict": "True",
    },
    {
        "claim": "A WhatsApp forward says a foreign minister resigned 10 minutes ago; no ministry statement exists yet.",
        "evidence": "No official confirmation is available at the time of the claim.",
        "verdict": "Insufficient Evidence",
    },
    {
        "claim": "Tariffs are taxes on imported goods.",
        "evidence": "A tariff is a customs duty levied on imports (sometimes exports).",
        "verdict": "True",
    },
    {
        "claim": "All government debt is illegal in every country and cannot exist.",
        "evidence": "Sovereign debt is a standard feature of public finance in most countries.",
        "verdict": "False",
    },
    {
        "claim": "The Universal Declaration of Human Rights was adopted by the UN in 1948.",
        "evidence": "The UDHR was adopted by the UN General Assembly on 10 December 1948.",
        "verdict": "True",
    },
    {
        "claim": "A blog claims a new tax rate of 0% for everyone is already in the official gazette, but no gazette page is linked.",
        "evidence": "Tax law changes require published legislation. Unsourced posts are not proof.",
        "verdict": "Insufficient Evidence",
    },
    {
        "claim": "Separation of powers typically refers to dividing legislative, executive, and judicial functions.",
        "evidence": "Constitutional theory distinguishes these branches to limit concentrated authority.",
        "verdict": "True",
    },
]

GENERAL = [
    {
        "claim": "The Great Wall of China is visible from space with the naked eye.",
        "evidence": "NASA and astronauts report the Wall is not readily visible to the unaided eye from space, unlike cities or coastlines.",
        "verdict": "False",
    },
    {
        "claim": "Goldfish have a three-second memory.",
        "evidence": "Studies show goldfish can remember information for months, not three seconds.",
        "verdict": "False",
    },
    {
        "claim": "Bulls are enraged by the color red in bullfighting.",
        "evidence": "Cattle are dichromatic; the muleta's motion, not redness, is the main stimulus. Bulls do not specially hate red.",
        "verdict": "False",
    },
    {
        "claim": "Mount Everest is Earth's highest mountain above sea level.",
        "evidence": "Everest's summit is about 8,849 m above sea level, the highest.",
        "verdict": "True",
    },
    {
        "claim": "The Amazon River is one of the world's largest rivers by discharge.",
        "evidence": "The Amazon has the largest discharge of any river.",
        "verdict": "True",
    },
    {
        "claim": "Napoleon Bonaparte was extremely short for his era, about 4 feet tall.",
        "evidence": "Napoleon's height was around 5'6\"–5'7\" in modern measure; the 'tiny Napoleon' story is a myth/unit confusion.",
        "verdict": "False",
    },
    {
        "claim": "The Titanic sank in 1912 after hitting an iceberg.",
        "evidence": "RMS Titanic sank on 15 April 1912 in the North Atlantic after an iceberg collision.",
        "verdict": "True",
    },
    {
        "claim": "Vikings wore horned helmets in battle as standard equipment.",
        "evidence": "Archaeology does not support horned battle helmets as Viking standard kit; the image is later romanticism.",
        "verdict": "False",
    },
    {
        "claim": "The Pacific Ocean is the largest ocean on Earth.",
        "evidence": "By area and volume, the Pacific is the largest ocean.",
        "verdict": "True",
    },
    {
        "claim": "Chameleons change color only for camouflage.",
        "evidence": "Color change also signals mood, temperature, and social status, not only camouflage.",
        "verdict": "Mostly True",
    },
    {
        "claim": "A viral chain message says you will have bad luck unless you forward it to 10 people.",
        "evidence": "Chain-letter luck claims have no empirical basis; they are social pressure scams/folklore.",
        "verdict": "False",
    },
    {
        "claim": "The Great Fire of London occurred in 1666.",
        "evidence": "Historical records date the Great Fire of London to 1666.",
        "verdict": "True",
    },
    {
        "claim": "Bats are blind.",
        "evidence": "Bats can see; many also use echolocation. 'Blind as a bat' is a misconception.",
        "verdict": "False",
    },
    {
        "claim": "The Sahara is a large desert in Africa.",
        "evidence": "The Sahara is the largest hot desert, spanning much of North Africa.",
        "verdict": "True",
    },
    {
        "claim": "A Facebook post claims a celebrity died this morning with no reputable news confirmation.",
        "evidence": "Death hoaxes are common. Without reliable reporting, the claim is unverified.",
        "verdict": "Insufficient Evidence",
    },
    {
        "claim": "Shaving hair makes it grow back thicker.",
        "evidence": "Shaving cuts hair at the blunt end, which can feel coarser, but does not change follicle thickness.",
        "verdict": "False",
    },
    {
        "claim": "Tokyo is the capital of Japan.",
        "evidence": "Tokyo is Japan's capital and largest city.",
        "verdict": "True",
    },
    {
        "claim": "The Bermuda Triangle has been scientifically proven to swallow ships via a unique supernatural force.",
        "evidence": "Investigations find no supernatural mechanism; traffic volume and weather explain many incidents.",
        "verdict": "False",
    },
    {
        "claim": "Penguins live in the Antarctic region (and some species elsewhere in the Southern Hemisphere).",
        "evidence": "Penguins are Southern Hemisphere birds; several species inhabit Antarctica and sub-Antarctic islands.",
        "verdict": "Mostly True",
    },
    {
        "claim": "The printing press associated with Gutenberg appeared in Europe in the 15th century.",
        "evidence": "Movable-type printing spread in Europe from the mid-1400s.",
        "verdict": "True",
    },
    {
        "claim": "You must wait 24 hours to report a missing person.",
        "evidence": "Law enforcement typically encourages reporting immediately; the 24-hour rule is a myth.",
        "verdict": "False",
    },
    {
        "claim": "The Nile flows through northeastern Africa.",
        "evidence": "The Nile is a major northeast African river flowing toward the Mediterranean.",
        "verdict": "True",
    },
    {
        "claim": "An anonymous forum post says a new continent rose in the Atlantic yesterday.",
        "evidence": "No geological agency reported a new continent. The claim lacks corroboration.",
        "verdict": "Insufficient Evidence",
    },
    {
        "claim": "Fortune cookies were invented in ancient China as imperial decrees.",
        "evidence": "Fortune cookies are associated with Japanese-American and Chinese-American restaurants in the US, not ancient Chinese imperial practice.",
        "verdict": "False",
    },
    {
        "claim": "The Eiffel Tower is in Paris, France.",
        "evidence": "The Eiffel Tower is a landmark on the Champ de Mars in Paris.",
        "verdict": "True",
    },
    {
        "claim": "Swallowed chewing gum stays in your stomach for seven years.",
        "evidence": "Gum is not digested like food but typically passes through the digestive tract, not remaining seven years.",
        "verdict": "False",
    },
    {
        "claim": "The Olympic Games originated in ancient Greece.",
        "evidence": "Ancient Olympics were held at Olympia in Greece; the modern Games began in 1896.",
        "verdict": "True",
    },
    {
        "claim": "A WhatsApp screenshot claims all birds disappeared worldwide last night.",
        "evidence": "Ornithological networks would document a global bird disappearance. No such event is recorded.",
        "verdict": "False",
    },
    {
        "claim": "The Library of Alexandria's complete catalog survives intact today.",
        "evidence": "The ancient library did not survive intact; its holdings and destruction are incompletely documented.",
        "verdict": "False",
    },
    {
        "claim": "Water is wet in the ordinary-language sense that liquid water makes things wet.",
        "evidence": "This is a semantic debate more than a factual one; liquid water causes wetting of surfaces.",
        "verdict": "Mostly True",
    },
    {
        "claim": "The internet was developed from earlier packet-switched networks including ARPANET.",
        "evidence": "ARPANET and related research networks are ancestors of the modern internet.",
        "verdict": "True",
    },
    {
        "claim": "A rumor says a specific living person was knighted yesterday; no honors list is published.",
        "evidence": "Official honors are published. Without a list, knighthood claims are unverified.",
        "verdict": "Insufficient Evidence",
    },
    {
        "claim": "Camels store water in their humps.",
        "evidence": "Humps store fat, not water. Camels are adapted to conserve water in other ways.",
        "verdict": "False",
    },
    {
        "claim": "Shakespeare is credited as the author of Hamlet.",
        "evidence": "Hamlet is a play attributed to William Shakespeare.",
        "verdict": "True",
    },
    {
        "claim": "The dark side of the Moon never receives sunlight.",
        "evidence": "The far side of the Moon is not always dark; both sides have day/night. Tidal locking hides one face from Earth.",
        "verdict": "False",
    },
    {
        "claim": "Coffee is made from roasted coffee beans, which are seeds of the coffee plant.",
        "evidence": "Coffee beans are seeds from Coffea cherries, roasted and brewed.",
        "verdict": "True",
    },
    {
        "claim": "A chain post says a supermarket will give free cars to anyone who comments 'YES'.",
        "evidence": "Engagement-bait giveaway posts of this type are typically scams, not official promotions.",
        "verdict": "False",
    },
    {
        "claim": "The compass points toward magnetic north, which is not exactly the same as geographic north.",
        "evidence": "Magnetic declination means compass north differs from true north depending on location.",
        "verdict": "True",
    },
    {
        "claim": "Tomatoes are botanically fruits but often used as vegetables in cooking.",
        "evidence": "Botanically fruits (ovary-derived); culinary classification as vegetables is common.",
        "verdict": "True",
    },
    {
        "claim": "Someone on a forum claims they time-traveled and met a president in 1890, with no corroboration.",
        "evidence": "Anecdotes of time travel are not verifiable evidence.",
        "verdict": "Insufficient Evidence",
    },
]

SEED_BY_AGENT = {
    "science": SCIENCE,
    "health": HEALTH,
    "politics": POLITICS,
    "general": GENERAL,
}
