"""Génère la grille Excel complétée et les fichiers de données LaTeX.

Usage : python3 scripts/generer.py
"""
import datetime as dt
import shutil
from pathlib import Path

import openpyxl
from openpyxl.styles import Alignment

import donnees as D

RACINE = Path(__file__).resolve().parent.parent
MODELE = RACINE / "scripts" / "modele" / "04_Grille_Audit_SSI.xlsx"
SORTIE_XLSX = RACINE / "livrables" / "MEDICA-SERVICES_Grille_Audit_SSI_completee.xlsx"
DONNEES_TEX = [RACINE / "src" / "rapport" / "donnees", RACINE / "src" / "guide" / "donnees"]

CONSTATS = {c["id"]: c for c in D.CONSTATS}


# ---------------------------------------------------------------------------
# Calculs de contrôle (reproduisent les formules de la grille)
# ---------------------------------------------------------------------------
def calculs():
    maxima, somme, niveau, cible = D.calcul_cible()
    for code, cout in D.COUTS.items():
        assert code in D.ACTIONS, code
    total = sum(D.COUTS[a] * D.ACTIONS[a][2] for a in D.ACTIONS)
    assert total <= D.PLAFOND, "dépassement du plafond"
    return dict(maxima=maxima, somme=somme, niveau=niveau, cible=cible, total=total, marge=D.PLAFOND - total)


# ---------------------------------------------------------------------------
# Excel
# ---------------------------------------------------------------------------
def remplir_excel(k):
    wb = openpyxl.load_workbook(MODELE)
    wrap = Alignment(wrap_text=True, vertical="top")

    ws = wb["01_AUTODIAGNOSTIC"]
    for i, (qid, intitule, note, refs, just, conf) in enumerate(D.QUESTIONS, start=2):
        assert ws[f"A{i}"].value == qid and ws[f"B{i}"].value == intitule, (qid, ws[f"B{i}"].value)
        ws[f"C{i}"] = note
        ws[f"D{i}"] = refs
        ws[f"E{i}"] = just
        ws[f"F{i}"] = conf
        for col in "DE":
            ws[f"{col}{i}"].alignment = wrap
    ws["B22"] = D.AJUSTEMENT

    ws = wb["02_MATURITE_EFFECTIVE"]
    for i, p in enumerate(D.PROCESSUS, start=2):
        assert ws[f"A{i}"].value == p["nom"], (p["nom"], ws[f"A{i}"].value)
        ws[f"B{i}"] = p["revendique"]
        ws[f"C{i}"] = p["effectif"]
        ws[f"D{i}"] = p["preuves"]
        ws[f"E{i}"] = p["reserve"]
        ws[f"G{i}"] = p["progression"]
        for col in "DEG":
            ws[f"{col}{i}"].alignment = wrap

    ws = wb["03_CONSTATS_TECHNIQUES"]
    for i, c in enumerate(D.CONSTATS, start=2):
        assert ws[f"A{i}"].value == c["id"]
        valeurs = [c["pieces"], c["observation"], c["reserve"], c["processus"], c["scenario"],
                   c["priorite"], c["reco"], c["cloture"]]
        for col, v in zip("BCDEFGHI", valeurs):
            ws[f"{col}{i}"] = v
            ws[f"{col}{i}"].alignment = wrap

    ws = wb["04_REGISTRE_RISQUES"]
    for i, r in enumerate(D.RISQUES, start=2):
        assert ws[f"A{i}"].value == r["id"]
        valeurs = {"B": r["evenement"], "C": r["actif"], "D": r["menace"], "E": r["vuln"], "F": r["mesures"],
                   "G": r["impact"], "H": r["vrais"], "J": r["decision"], "K": r["preuves"]}
        for col, v in valeurs.items():
            ws[f"{col}{i}"] = v
            if isinstance(v, str):
                ws[f"{col}{i}"].alignment = wrap

    ws = wb["05_PLAN_ACTION"]
    for i in range(2, 13):
        code = ws[f"A{i}"].value
        assert ws[f"D{i}"].value == D.COUTS[code], code
        pilote, echeance, retenu, just, _ = D.ACTIONS[code]
        ws[f"E{i}"] = pilote
        ws[f"F{i}"] = echeance
        ws[f"G{i}"] = retenu
        ws[f"H{i}"] = just
        for col in "FH":
            ws[f"{col}{i}"].alignment = wrap

    # 06_BAREME reste vierge : réservé à l'enseignant.
    from openpyxl.workbook.properties import CalcProperties
    wb.calculation = CalcProperties(fullCalcOnLoad=True)
    SORTIE_XLSX.parent.mkdir(exist_ok=True)
    wb.save(SORTIE_XLSX)


# ---------------------------------------------------------------------------
# LaTeX
# ---------------------------------------------------------------------------
def tex(s):
    s = str(s)
    for a, b in [("\\", r"\textbackslash{}"), ("&", r"\&"), ("%", r"\%"), ("#", r"\#"), ("_", r"\_"),
                 ("$", r"\$"), ("{", r"\{"), ("}", r"\}")]:
        s = s.replace(a, b)
    return s


def pieces(s):
    return tex(s).replace("/", "/\\allowbreak{}")


def euros(n):
    return f"{n:,}".replace(",", "\\,") + "\\,€"


def defn(nom, valeur):
    return f"\\expandafter\\def\\csname {nom}\\endcsname{{{valeur}}}\n"


def ecrire(nom, contenu):
    for d in DONNEES_TEX:
        d.mkdir(parents=True, exist_ok=True)
        (d / nom).write_text(contenu, encoding="utf-8")


def date(s):
    return dt.date.fromisoformat(s)


def generer_tex(k):
    m = ["% Fichier généré par scripts/generer.py depuis scripts/donnees.py. Ne pas éditer à la main.\n"]
    m.append(f"\\newcommand\\Cible{{{k['cible']}}}\n\\newcommand\\NiveauCalcule{{{k['niveau']}}}\n")
    m.append(f"\\newcommand\\SommeMaxima{{{k['somme']}}}\n\\newcommand\\Ajustement{{{D.AJUSTEMENT}}}\n")
    for (nom, _, _), v, macro in zip(D.GROUPES, k["maxima"], ["MaxConseq", "MaxSensib", "MaxMenaces", "MaxVuln"]):
        m.append(f"\\newcommand\\{macro}{{{v}}}\n")
    m.append(f"\\newcommand\\Plafond{{{euros(D.PLAFOND)}}}\n\\newcommand\\TotalRetenu{{{euros(k['total'])}}}\n")
    m.append(f"\\newcommand\\Marge{{{euros(k['marge'])}}}\n")
    m.append("\\newcommand\\qnote[1]{\\csname qnote#1\\endcsname}\n")
    m.append("\\newcommand\\peff[1]{\\csname peff#1\\endcsname}\n")
    m.append("\\newcommand\\rimp[1]{\\csname rimp#1\\endcsname}\n\\newcommand\\rvra[1]{\\csname rvra#1\\endcsname}\n")
    m.append("\\newcommand\\rscore[1]{\\csname rscore#1\\endcsname}\n\\newcommand\\acout[1]{\\csname acout#1\\endcsname}\n")
    for q in D.QUESTIONS:
        m.append(defn(f"qnote{q[0]}", q[2]))
    for p in D.PROCESSUS:
        m.append(defn(f"peff{p['court']}", p["effectif"]))
    for r in D.RISQUES:
        m.append(defn(f"rimp{r['id']}", r["impact"]) + defn(f"rvra{r['id']}", r["vrais"]))
        m.append(defn(f"rscore{r['id']}", r["impact"] * r["vrais"]))
    for a, c in D.COUTS.items():
        m.append(defn(f"acout{a}", euros(c)))
    ecrire("macros.tex", "".join(m))

    # Tableau Q01 à Q12
    lignes = []
    for qid, intitule, note, refs, just, conf in D.QUESTIONS:
        lignes.append(f"{qid} & {tex(intitule)} & \\textbf{{{note}}} & {tex(refs)} & {tex(just)} & {tex(conf)} \\\\\n")
    ecrire("tab_questions.tex", "".join(lignes))

    # Tableau des maxima
    lignes = []
    for (nom, plage, _), v in zip(D.GROUPES, k["maxima"]):
        lignes.append(f"{tex(nom)} & {plage} & {v} \\\\\n")
    ecrire("tab_maxima.tex", "".join(lignes))

    # Processus
    lignes = []
    for p in D.PROCESSUS:
        ecart = max(0, k["cible"] - p["effectif"])
        lignes.append(f"{tex(p['nom'])} & {tex(p['revendique'])} & \\textbf{{{p['effectif']}}} & {tex(p['suivant'])} & "
                      f"{tex(p['preuves'])} & {ecart} \\\\\n")
    ecrire("tab_processus.tex", "".join(lignes))
    lignes = []
    for p in D.PROCESSUS:
        lignes.append(f"{tex(p['nom'])} & {tex(p['preuves'])} & {tex(p['reserve'])} & {tex(p['progression'])} \\\\\n")
    ecrire("tab_processus_detail.tex", "".join(lignes))
    coords = " ".join(f"({p['effectif']},{i})" for i, p in enumerate(D.PROCESSUS, start=1))
    noms = ",".join(tex(p["court"]) for p in D.PROCESSUS)
    ecrire("graph_maturite.tex", f"\\def\\MaturiteNoms{{{noms}}}\n\\def\\MaturiteNb{{{len(D.PROCESSUS)}}}\n"
           f"\\def\\MaturitePlot{{\\addplot[draw=accent, fill=accent] coordinates {{{coords}}};}}\n")

    # Constats (complet) et corrélation T5
    lignes = []
    for c in D.CONSTATS:
        lignes.append(f"{c['id']} & {pieces(c['pieces'])} & {tex(c['observation'])} & {tex(c['reserve'])} & "
                      f"{tex(c['priorite'])} \\\\\n")
    ecrire("tab_constats.tex", "".join(lignes))
    lignes = []
    for c in D.CONSTATS:
        lignes.append(f"{c['id']} & {tex(c['processus'])} & {tex(c['scenario'])} & {tex(c['reco'])} & {tex(c['cloture'])} \\\\\n")
    ecrire("tab_constats_suite.tex", "".join(lignes))
    lignes = []
    for cid in D.CORRELATIONS:
        c = CONSTATS[cid]
        lignes.append(f"{cid} {tex(c['titre'])} & {pieces(c['pieces'])} & {c['risque']} & {tex(c['processus'])} & "
                      f"{tex(c['niveau'])} & {tex(c['action'])} & {tex(c['pilote'])} & {tex(c['cloture'])} \\\\\n")
    ecrire("tab_correlation.tex", "".join(lignes))

    # Risques
    lignes = []
    for r in D.RISQUES:
        lignes.append(f"{r['id']} & {tex(r['evenement'])} & {tex(r['actif'])} & {tex(r['vuln'])} & {r['impact']} & {r['vrais']} & "
                      f"\\textbf{{{r['impact'] * r['vrais']}}} & {tex(r['decision'])} \\\\\n")
    ecrire("tab_risques.tex", "".join(lignes))
    lignes = []
    for r in D.RISQUES:
        lignes.append(f"{r['id']} & {tex(r['menace'])} & {tex(r['mesures'])} & {tex(r['preuves'])} \\\\\n")
    ecrire("tab_risques_suite.tex", "".join(lignes))
    cases = {}
    for r in D.RISQUES:
        cases.setdefault((r["impact"], r["vrais"]), []).append(r["id"])
    pts = "".join(f"\\RisqueCase{{{v}}}{{{i}}}{{{', '.join(ids)}}}\n" for (i, v), ids in cases.items())
    ecrire("graph_risques.tex", pts)

    # Actions
    lignes = []
    for code in D.COUTS:
        pilote, echeance, retenu, just, court = D.ACTIONS[code]
        etat = "\\Retenu" if retenu else "\\Differe"
        lignes.append(f"{code} & {tex(court)} & {euros(D.COUTS[code])} & {etat} & {tex(pilote)} & {tex(echeance)} & {tex(just)} \\\\\n")
    ecrire("tab_actions.tex", "".join(lignes))

    # Feuille de route SSI (12 mois)
    lignes = []
    for libelle, debut, fin, livrable in D.FEUILLE_ROUTE:
        lignes.append(f"\\FeuilleRoute{{{tex(libelle)}}}{{{debut + 1}}}{{{fin}}}{{{tex(livrable)}}}\n")
    ecrire("gantt_feuille_route.tex", "".join(lignes))
    lignes = []
    for nom, (m6, m12) in D.TRAJECTOIRE.items():
        eff = next(p["effectif"] for p in D.PROCESSUS if p["court"] == nom)
        lignes.append(f"{tex(nom)} & {eff} & {m6} & {m12} & {k['cible']} \\\\\n")
    ecrire("tab_trajectoire.tex", "".join(lignes))

    # Gantt du projet
    debut = date("2026-10-20")
    lignes, liens = [], []
    for tid, lib, resp, d0, d1, deps, _ in D.TACHES:
        a, b = (date(d0) - debut).days + 1, (date(d1) - debut).days + 1
        lignes.append(f"\\TacheGantt{{{tid}}}{{{tex(lib)}}}{{{tex(resp)}}}{{{a}}}{{{b}}}\n")
        for dep in deps:
            liens.append(f"\\LienDD{{{dep}}}{{{tid}}}\n")
    for jid, lib, d in D.JALONS:
        a = (date(d) - debut).days + 1
        lignes.append(f"\\JalonGantt{{{jid}}}{{{tex(lib)}}}{{{a}}}\n")
    ecrire("gantt_projet.tex", "".join(lignes) + "".join(liens))

    # Kanban projeté
    colonnes = ["À faire", "En cours", "À relire", "À corriger", "Validé"]
    lignes = []
    for tid, lib, resp, *_rest, col in D.TACHES:
        assert col in colonnes, col
        lignes.append(f"\\CarteKanban{{{colonnes.index(col)}}}{{{tid}}}{{{tex(lib)}}}{{{tex(resp)}}}\n")
    ecrire("kanban.tex", "".join(lignes))

    # Tableau des tâches (correspondance Gantt et Kanban)
    lignes = []
    for tid, lib, resp, d0, d1, deps, col in D.TACHES:
        f = lambda s: date(s).strftime("%d/%m")
        lignes.append(f"{tid} & {tex(lib)} & {tex(resp)} & {f(d0)} au {f(d1)} & {', '.join(deps) or '·'} & {tex(col)} (initial) & à renseigner \\\\\n")
    ecrire("tab_taches.tex", "".join(lignes))


def main():
    k = calculs()
    if not MODELE.exists():
        raise SystemExit(f"Modèle introuvable : {MODELE}")
    remplir_excel(k)
    generer_tex(k)
    print(f"Cible {k['cible']} (somme {k['somme']}, maxima {k['maxima']}), engagement {k['total']} €, marge {k['marge']} €")


if __name__ == "__main__":
    main()
