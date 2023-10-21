import copy
import csv
import re
from cockatoo import screen
from cockatoo import metric


class DistanceMetric():
    def __init__(self):
        self.smiles = {}
        self.molecular_weights = {}
        self.density = {}
        self.fingerprints = {}
        self.compounds = {}
        self.cocktails = {}
        self.data = []

        print "Metric loading"

        with open('hwi-compounds2.csv') as fh:
            reader = csv.DictReader(fh, delimiter=";")
            for row in reader:
                self.data.append(row)
                # print(row)
                if len(row['smiles']) == 0:
                    continue
                name = row['name'].lower()
                self.smiles[name] = row['smiles']
                self.molecular_weights[name] = row['molecular_weight']
                self.density[name] = row['density']

                compound = screen.Compound(name.encode('utf-8'), row['conc_min'], "M")
                setattr(compound, "molecular_weight", row["molecular_weight"])
                setattr(compound, "smiles", row["smiles"])

                # print compound.name, compound.fingerprint()
                self.fingerprints[name] = compound.fingerprint()
                compound.fingerprint_cached = self.fingerprints[name]
                self.compounds[name] = compound
        print "Metric loaded"
        # print [c['name'] for c in self.data]


    def get_dict(self, names, ph):
        # print names, ph
        tail = {"name": "8_C0160", "ph": ph}
        rows = []
        for name in names:
            row = {}
            conc = None
            try:
                conc = name[1]
            except:
                pass
            name = name[0].lower()
            if (name not in self.compounds.keys()) and (name not in self.not_ins):
                self.not_ins.append(name)
                print name
            if name[:19] == 'polyethylene glycol':
                name = 'polyethylene glycol 200'
            smile = [c['smiles'] for c in self.data if c['name'].lower() == name][0]
            molecular_weight = [c['molecular_weight'] for c in self.data if c['name'].lower() == name][0]
            conc_min = [c['conc_min'] for c in self.data if c['name'].lower() == name][0]
            row["smiles"] = smile
            row["name"] = name
            # print molecular_weight
            if molecular_weight == "":
                molecular_weight = 0.0
            row["molecular_weight"] = float(molecular_weight)
            row["unit"] = "M"
            if conc is None: conc = conc_min
            row["conc"] = conc
            rows.append(row)

        tail["components"] = rows

        return tail

    def get_distance(self, cocktail1, cocktail2):
        key1 = " ".join(c[0] for c in cocktail1[0])
        key2 = " ".join(c[0] for c in cocktail2[0])

        if cocktail1[1] is not None:
            key1 += " " + str(cocktail1[1])

        if cocktail2[1] is not None:
            key2 += " "+ str(cocktail2[1])

        if key1 in self.cocktails:
            ck1 = self.cocktails[key1]
        else:
            ck1 = self.get_dict(cocktail1[0], cocktail1[1])
            ck1 = self.parse_cocktail_json(ck1)
            self.cocktails[key1] = copy.deepcopy(ck1)

        # print "===============--=-=-=-=-=-="

        if key2 in self.cocktails:
            ck2 = self.cocktails[key2]
        else:
            ck2 = self.get_dict(cocktail2[0], cocktail2[1])
            ck2 = self.parse_cocktail_json(ck2)
            self.cocktails[key2] = copy.deepcopy(ck2)

        # print(ck1.components, ck2.components)

        return metric.distance(ck1, ck2)

    def parse_cocktail_json(self, ck):
        # cocktail = self.cocktails[ck['name']]
        # return cocktail

        cocktail = screen.Cocktail(ck['name'])
        # print(cocktail)
        for key in cocktail.__dict__.keys():
            if key == 'components' or key.startswith('_'): continue
            if key not in ck:
                # logger.debug('Invalid json, missing cocktail attribute %s: ' % key)
                continue
            setattr(cocktail, key, ck[key])
        # print(cocktail)

        for cp in ck['components']:
                is_valid = True
                for key in ('conc', 'molecular_weight', 'name', 'smiles', 'unit'):
                    if key not in cp:
                        # logger.critical('Invalid json, cocktail %s has compound missing required value %s: ' % (cocktail.name, key))
                        is_valid = False

                if not is_valid:
                    print("not valid")
                    return None

                compound = self.compounds[cp['name'].encode('utf-8')]
                # compound = screen.Compound(cp['name'].encode('utf-8'), cp['conc'], cp['unit'])
                # for key in compound.__dict__.keys():
                #     if key.startswith('_'): continue
                #     if key not in cp:
                #         continue
                #     # print key, cp[key]
                #     setattr(compound, key, cp[key])

                # compound.fingerprint_cached = self.fingerprints[cp['name']]

                # handle special case for tacsimate
                if re.search(r'tacsimate', compound.name, re.IGNORECASE):
                    if not re.search(r'v\/v', compound.unit, re.IGNORECASE):
                        # logger.warning('Malformed line, tacsimate should be % v/v: {}'.format(compound))
                        print('Malformed line, tacsimate should be % v/v: {}'.format(compound))
                        return None
                    for c in screen._create_tacsimate(compound):
                        cocktail.add_compound(c)
                else:
                    cocktail.add_compound(compound)

        return cocktail
