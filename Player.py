class Player:
    def __init__(self,  name, surname, date, place, ci, cat, shirt_size):
        self.name = name
        self.surname = surname
        self.date = date
        self.place = place
        self.ci = ci
        self.cat = cat
        self.shirt_size = shirt_size

    def to_string(self):
        # Nome,Cognome,Data di nascita,Luogo di nascita,Autorizzazione dei genitori,
        # Certificato medico,Carta d'identità,Foto della carta d'identità fronte-retro,Tesserato/Categoria
        print(f"\t{self.name}"
              f"\t{self.surname}"
              f"\t{self.date}"
              f"\t{self.place}"
              f"\t{self.ci}"
              f"\t{self.cat}"
              f"\t{self.shirt_size}\n")

    def to_dict(self):
        # print("\tNOME\tCOGNOME\tDATA DI NASCITA\tLUOGO DI NASCITA\tAUTH\tCERT\tCARTA IDENTITà\tFOTO\tCATEGORIA\n")
        p = {
            "NOME": self.name,
            "COGNOME": self.surname,
            "DATA DI NASCITA": self.date,
            "LUOGO DI NASCITA": self.place,
            "CARTA IDENTITA'": self.ci,
            "CATEGORIA": self.cat,
            "MAGLIETTA": self.shirt_size,
        }
        return p