let NEU = true;

function ch(a, n) {
    return NEU ? n : a;
}

function setModules(vertiefung, vertiefung2) {
    // $.post('http://localhost:8000/link/zum/endpunkt', {
    //     vertiefung_1: vertiefung,
    //     vertiefung_2: vertiefung2
    // }).done(function(data) {
    //     modules = data;
    // });

    modules['4INFBA001'] = ['Diskrete Mathematik', 9, WiSe, [],
        [], 1, 101, 'P'
    ]
    modules['4MATHBAEX01'] = ['Mathematik I', 9, SoSe, [],
        [], 2, 102, 'P'
    ]
    modules['4INFBA002'] = ['Vertiefung Mathematik', 6, WiSe, ['4MATHBAEX01'],
        [], 3, 103, 'P'
    ]
    modules['4INFBA003'] = ['Algorithmen und Datenstrukturen', 9, WiSe, [],
        [], 4, 104, 'P'
    ]
    modules['4INFBA004'] = ['Objektorientierung und funktionale Programmierung', 9, SoSe, [],
        [], 5, 105, 'P'
    ]
    modules['4INFBA005'] = ['Formale Sprachen und Automaten', 6, SoSe, [],
        [], 6, 606, 'P'
    ]
    modules['4INFBA006'] = ['Berechenbarkeit und Logik', 6, WiSe, ['4INFBA005'],
        [], 7, 607, 'P'
    ]
    modules['4INFBA007'] = ['Softwaretechnik I', 6, WiSe, ['4INFBA004'],
        [], 8, 608, 'P'
    ]
    modules['4INFBA008'] = ['Datenbanksysteme I', 6, WiSe, [],
        [], 9, 609, 'P'
    ]
    modules['4INFBA009'] = ['Digitaltechnik', 6, WiSe, [],
        [], 10, 510, 'P'
    ]
    modules['4INFBA010'] = ['Rechnerarchitekturen I', 6, SoSe, ['4INFBA009'],
        [], 11, 611, 'P'
    ]
    modules['4INFBA011'] = ['Betriebssysteme und nebenläufige Programmierung', 6, ch(WiSe, SoSe), ['4INFBA003', '4INFBA004'],
        [], 12, 612, 'P'
    ]
    modules['4INFBA012'] = ['Rechnernetze I', 6, SoSe, [],
        [], 13, 613, 'P'
    ]
    modules['4INFBA013'] = ['Introduction to Machine Learning', 6, ch(WiSe, Jedes), ['4MATHBAEX01'],
        [], 14, 600, 'P'
    ]
    modules['4INFBA014'] = ['Hardware-Praktikum', 6, SoSe, ['4INFBA009'],
        [], 15, 515, 'P'
    ]
    modules['4INFBA015'] = ['Programmierpraktikum', 12, Jedes, ['4INFBA003', '4INFBA004'],
        [], 16, 316, 'P'
    ]
    modules['4INFBA016'] = ['Seminar Informatik', 6, Jedes, ['SEM3'],
        [], 17, 517, 'V'
    ]
    modules['4INFBA017'] = ['Bacheloararbeit', 12, Jedes, ['SEM4'],
        [], 90, 990, 'V'
    ]
    modules['4INFBA030'] = ['Praktikum Embedded Systems', 6, Jedes, ['4INFBA022'],
        [ES, CISS], 30, 630, 'V'
    ]
    modules['4INFBA031'] = ['Praktikum Rechnernetze', 6, WiSe, ['4INFBA012'],
        [ES, CISS], 31, 631, 'V'
    ]
    modules['4INFBA032'] = ['Praktikum Softwaretechnik', 6, SoSe, ['4INFBA003', '4INFBA004', '4INFBA015'],
        [ES, CISS], 32, 632, 'V'
    ]
    modules['4INFBA033'] = ['Praktikum Computergraphik', 6, ch(SoSe, WiSe), ['4INFBA020', '4INFBA200'],
        [ES, CISS, VC], 33, 433, 'V'
    ]
    modules['5DMTBA10'] = ['Praktikum Digitale Medizin', 6, WiSe, ['5DBHSBAEX01'],
        [ES, CISS, MI], 34, 634, 'V'
    ]
    if (vertiefung == VC || vertiefung2 == VC) {
        modules['4INFBA020'] = ['Einführung in Visual Computing', 6, ch(SoSe, WiSe), ['4MATHBAEX01'],
            [], 20, 220, 'G'
        ]
    }
    if (vertiefung == ES || vertiefung2 == ES) {
        modules['4INFBA022'] = ['Embedded Systems', 6, SoSe, ['4INFBA009'],
            [], 22, 222, 'G'
        ]
    }
    if (vertiefung == CISS || vertiefung2 == CISS) {
        modules['4INFBA021'] = ['Einführung in Complex and Intelligent Software Systems', 6, SoSe, [],
            [], 21, 221, 'G'
        ]
    }
    if (vertiefung == MI || vertiefung2 == MI) {
        modules['5DBHSBAEX01'] = ['Einführung in die medizinische Informatik', 6, WiSe, [],
            [], 23, 223, 'G'
        ]
    }
    if (vertiefung == VC) {
        modules['4INFBA200'] = ['Computergraphik', 6, ch(WiSe, SoSe), ['4INFBA020'],
            [], 40, 440, 'V'
        ]
        modules['4INFBA201'] = ['Digitale Bildverarbeitung', 6, ch(WiSe, SoSe), ['4MATHBAEX01', '4INFBA020'],
            [], 41, 441, 'V'
        ]
        modules['4INFBA202'] = ['Praktikum Digitale Bildverarbeitung', 6, ch(SoSe, WiSe), ['4INFBA020', '4INFBA201'],
            [], 42, 442, 'V'
        ]
        modules['VERT1'] = ['Vertiefungsmodul 1', 6, Jedes, ['4INFBA020'],
            [], 43, 743, 'V'
        ]
        modules['VERT2'] = ['Vertiefungsmodul 2', 6, Jedes, ['4INFBA020'],
            [], 44, 744, 'V'
        ]
    } else if (vertiefung == ES) {
        modules['VERT1'] = ['Vertiefungsmodul 1', 6, Jedes, ['4INFBA022'],
            [], 50, 750, 'V'
        ]
        modules['VERT2'] = ['Vertiefungsmodul 2', 6, Jedes, ['4INFBA022'],
            [], 51, 751, 'V'
        ]
        modules['VERT3'] = ['Vertiefungsmodul 3', 6, Jedes, ['4INFBA022'],
            [], 52, 752, 'V'
        ]
        modules['VERT4'] = ['Vertiefungsmodul 4', 6, Jedes, ['4INFBA022'],
            [], 53, 753, 'V'
        ]
        modules['VERT5'] = ['Vertiefungsmodul 5', 6, Jedes, ['4INFBA022'],
            [], 54, 754, 'V'
        ]
    } else if (vertiefung == CISS) {
        modules['VERT1'] = ['Vertiefungsmodul 1', 6, Jedes, ['4INFBA021', 'SEM3'],
            [], 60, 760, 'V'
        ]
        modules['VERT2'] = ['Vertiefungsmodul 2', 6, Jedes, ['4INFBA021', 'SEM3'],
            [], 61, 761, 'V'
        ]
        modules['VERT3'] = ['Vertiefungsmodul 3', 6, Jedes, ['4INFBA021', 'SEM3'],
            [], 62, 762, 'V'
        ]
        modules['VERT4'] = ['Vertiefungsmodul 4', 6, Jedes, ['4INFBA021', 'SEM3'],
            [], 63, 763, 'V'
        ]
        modules['VERT5'] = ['Vertiefungsmodul 5', 6, Jedes, ['4INFBA021', 'SEM3'],
            [], 64, 764, 'V'
        ]
    } else {
        modules['5DBHSBA01'] = ['Funktion Mensch  I', 9, WiSe, ['5DBHSBAEX01'],
            [], 70, 470, 'V'
        ]
        modules['5DBHSBA05'] = ['Apparative Diagnostik und Therapie', 6, WiSe, ['5DBHSBA01'],
            [], 71, 471, 'V'
        ]
        modules['5DBHSBAEX03'] = ['Praktikum Klinik-IT', 3, Jedes, ['5DBHSBAEX01'],
            [], 72, 472, 'V'
        ]
        modules['5DMTBA03'] = ['Strukturen des digitalen Gesundheitssystems', 6, SoSe, ['5DBHSBAEX01'],
            [], 73, 473, 'V'
        ]
        modules['VERT1'] = ['Vertiefungsmodul 1', 6, Jedes, ['5DBHSBAEX01'],
            [], 74, 774, 'V'
        ]
    }

    initializeModules();
}

let Jedes = 0,
    WiSe = 1,
    SoSe = 2,
    strSem = ['Jedes', 'WiSe', 'SoSe'],
    ES = 1,
    VC = 2,
    CISS = 3,
    MI = 4,
    strVert = ['??', 'ES', 'VC', 'CISS', 'MI'];

let vertiefungen = {
    'ES': ES,
    'VC': VC,
    'CISS': CISS,
    'MI': MI
}

let gewaehlteVertiefungen = [];
let gewaehltesSemester = null;

let gewaehlteFaecher = [];

let semesterPunktzahl = {
    "1": 0,
    "2": 0,
    "3": 0,
    "4": 0,
    "5": 0,
    "6": 0
}

let semesterAnzahl = null;
let modules = {};

function setUnselected(elementId) {
    document.getElementById(elementId).classList.remove('chosen');
}

function addModule(moduleId) {
    gewaehlteFaecher.push(moduleId);

    modules = modules.filter((e) => {
        return e[3] != moduleId;
    });
}

function initializeModules() {
    for (let i = 0; i < modules.length; i++) {

    }
}

function setSelected(elementId) {
    document.getElementById(elementId).classList.add('chosen');
}

function setSemester(semester) {
    setUnselected('semester_1');
    setUnselected('semester_2');

    gewaehltesSemester = semester;
    setSelected('semester_' + semester);
}

function setSemesterAnzahl(anzahl) {
    semesterAnzahl = anzahl;

    for (let i = 1; i < 9; i++) {
        setUnselected('semester_anzahl_' + i);
    }

    setSelected('semester_anzahl_' + anzahl);
}

function addVertiefung(vertiefung) {
    if (gewaehlteVertiefungen.indexOf(vertiefung) === -1 && gewaehlteVertiefungen.length < 2) {
        gewaehlteVertiefungen.push(vertiefung);
        setSelected('vertiefung_' + vertiefung);

        return;
    }

    if (gewaehlteVertiefungen.indexOf(vertiefung) !== -1) {
        setUnselected('vertiefung_' + vertiefung);
        gewaehlteVertiefungen = gewaehlteVertiefungen.filter(function(e) {
            return e !== vertiefung;
        });
    }
}

$("#example-basic").steps({
    headerTag: "h3",
    bodyTag: "section",
    transitionEffect: "slideLeft",
    labels: {
        next: "Weiter",
        previous: "Zurück",
        finish: "Fertig"
    },
    onStepChanged: function(event, currentIndex, newIndex) {},
    onStepChanging: function(event, currentIndex, newIndex) {
        if (currentIndex === 0) {
            if (gewaehltesSemester == null) {
                return false;
            }
        }

        if (currentIndex === 1) {
            if (gewaehlteVertiefungen.length != 2) {
                return false;
            }
        }

        if (currentIndex === 2) {
            if (semesterAnzahl == null) {
                return false;
            }

            initializeSemesterStart();
        }

        return true;
    },
    autoFocus: true
});

let template = `<li><a class="toggle" href="#" id="faecher_{IDENTIFIER}">{IDENTIFIER}. Semester {BEZEICHNUNG}</a><div class="inner">Fächer initialisieren</div></li>`;

function initializeSemesterStart() {
    let bezeichnungen = gewaehltesSemester === 1 ? ['WiSe', 'SoSe'] : ['SoSe', 'WiSe'];

    let semesterAccordion = '';

    for (let i = 1; i <= semesterAnzahl; i++) {
        semesterAccordion += template.replace("{IDENTIFIER}", i).replace("{IDENTIFIER}", i).replace("{BEZEICHNUNG}", '(' + bezeichnungen[(i - 1) % 2] + ')');
    }

    document.getElementById('accordion').innerHTML = semesterAccordion;

    $('.toggle').click(function(e) {
        e.preventDefault();

        let $this = $(this);

        if ($this.next().hasClass('show')) {
            $this.next().removeClass('show');
            $this.next().slideUp(350);
        } else {
            $this.parent().parent().find('li .inner').removeClass('show');
            $this.parent().parent().find('li .inner').slideUp(350);
            $this.next().toggleClass('show');
            $this.next().slideToggle(350);
        }
    });

    setModules(gewaehlteVertiefungen[0], gewaehlteVertiefungen[1]);
}