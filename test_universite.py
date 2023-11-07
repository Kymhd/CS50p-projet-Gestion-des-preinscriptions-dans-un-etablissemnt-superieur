from universite import Universite

#Test pour la classe Universite, "monkeypatch" c'est pour simuler les entrées

def test_choisir_serie(monkeypatch):
    """ Test sur choisir une Serie"""
    universite = Universite()
    monkeypatch.setattr('builtins.input', lambda _: "D")
    universite.choisir_serie()
    assert universite.serie == "D"

def test_choisir_faculte(monkeypatch, capsys):
    """ Test sur choisir une faculté"""
    universite = Universite()
    universite.serie = "D"
    monkeypatch.setattr('builtins.input', lambda _: "2")
    universite.choisir_faculte()
    captured = capsys.readouterr()
    assert universite.faculte == "Institut Universitaire de Technologie (IUT)"
    assert "Les facultés disponibles pour votre série sont :" in captured.out

def test_choisir_departement(monkeypatch, capsys):
    """ Test sur choisir une le deparrtement liés à la Faculté"""
    universite = Universite()
    universite.faculte = "Institut Universitaire de Technologie (IUT)"
    monkeypatch.setattr('builtins.input', lambda _: "3")
    universite.choisir_departement()
    captured = capsys.readouterr()
    assert universite.departement == "Génie Informatique"
    assert f"Les départements de la faculté '{universite.faculte}' sont :" in captured.out
