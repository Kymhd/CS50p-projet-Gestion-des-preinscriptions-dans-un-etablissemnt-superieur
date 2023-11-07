from universite import Universite

def test_choisir_serie(monkeypatch):
    universite = Universite()
    monkeypatch.setattr('builtins.input', lambda _: "S")
    universite.choisir_serie()
    assert universite.serie == "S"

def test_choisir_faculte(monkeypatch, capsys):
    universite = Universite()
    universite.serie = "C"
    monkeypatch.setattr('builtins.input', lambda _: "2")
    universite.choisir_faculte()
    captured = capsys.readouterr()
    assert universite.faculte == "Ecole polytetchnique"
    assert "Les facultés disponibles pour votre série sont :" in captured.out

def test_choisir_departement(monkeypatch, capsys):
    universite = Universite()
    universite.faculte = "Faculté d'Informatique"
    monkeypatch.setattr('builtins.input', lambda _: "1")
    universite.choisir_departement()
    captured = capsys.readouterr()
    assert universite.departement == "Informatique"
    assert f"Les départements de la faculté '{universite.faculte}' sont :" in captured.out
