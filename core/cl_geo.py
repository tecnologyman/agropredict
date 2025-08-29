# core/cl_geo.py
# -*- coding: utf-8 -*-

from django.utils.text import slugify as dj_slugify

REGIONES = [
    ("Arica y Parinacota", "Arica y Parinacota"),
    ("Tarapacá", "Tarapacá"),
    ("Antofagasta", "Antofagasta"),
    ("Atacama", "Atacama"),
    ("Coquimbo", "Coquimbo"),
    ("Valparaíso", "Valparaíso"),
    ("Metropolitana", "Metropolitana"),
    ("O’Higgins", "O’Higgins"),
    ("Maule", "Maule"),
    ("Ñuble", "Ñuble"),
    ("Biobío", "Biobío"),
    ("La Araucanía", "La Araucanía"),
    ("Los Ríos", "Los Ríos"),
    ("Los Lagos", "Los Lagos"),
    ("Aysén", "Aysén"),
    ("Magallanes", "Magallanes"),
]

COMUNAS_POR_REGION = {
    "Arica y Parinacota": [
        "Arica","Camarones","Putre","General Lagos"
    ],
    "Tarapacá": [
        "Iquique","Alto Hospicio","Pozo Almonte","Camiña","Colchane","Huara","Pica"
    ],
    "Antofagasta": [
        "Antofagasta","Mejillones","Sierra Gorda","Taltal",
        "Calama","Ollagüe","San Pedro de Atacama",
        "Tocopilla","María Elena"
    ],
    "Atacama": [
        "Copiapó","Caldera","Tierra Amarilla",
        "Chañaral","Diego de Almagro",
        "Vallenar","Freirina","Huasco","Alto del Carmen"
    ],
    "Coquimbo": [
        "La Serena","Coquimbo","Andacollo","La Higuera","Paihuano","Vicuña",
        "Illapel","Canela","Los Vilos","Salamanca",
        "Ovalle","Combarbalá","Monte Patria","Punitaqui","Río Hurtado"
    ],
    "Valparaíso": [
        "Valparaíso","Viña del Mar","Concón","Quintero","Puchuncaví","Casablanca","Juan Fernández",
        "San Antonio","Cartagena","El Tabo","El Quisco","Algarrobo","Santo Domingo",
        "Los Andes","San Esteban","Calle Larga","Rinconada",
        "San Felipe","Llaillay","Catemu","Panquehue","Putaendo","Santa María",
        "Quillota","La Calera","La Cruz","Hijuelas","Nogales",
        "Quilpué","Villa Alemana","Limache","Olmué",
        "Petorca","La Ligua","Cabildo","Papudo","Zapallar",
        "Isla de Pascua"
    ],
    "Metropolitana": [
        # Provincia de Santiago
        "Santiago","Cerrillos","Cerro Navia","Conchalí","El Bosque","Estación Central","Huechuraba",
        "Independencia","La Cisterna","La Florida","La Granja","La Pintana","La Reina","Las Condes",
        "Lo Barnechea","Lo Espejo","Lo Prado","Macul","Maipú","Ñuñoa","Pedro Aguirre Cerda",
        "Peñalolén","Providencia","Pudahuel","Quilicura","Quinta Normal","Recoleta","Renca",
        "San Joaquín","San Miguel","San Ramón","Vitacura",
        # Cordillera
        "Puente Alto","San José de Maipo","Pirque",
        # Chacabuco
        "Colina","Lampa","Tiltil",
        # Maipo
        "San Bernardo","Buin","Paine","Calera de Tango",
        # Talagante
        "Talagante","Peñaflor","Isla de Maipo","El Monte","Padre Hurtado",
        # Melipilla
        "Melipilla","Curacaví","María Pinto","San Pedro","Alhué"
    ],
    "O’Higgins": [
        "Rancagua","Machalí","Graneros","Mostazal","Codegua","Requínoa","Doñihue","Coinco","Coltauco",
        "Quinta de Tilcoco","Rengo","Malloa","San Vicente","Pichidegua","Las Cabras","Peumo",
        "San Fernando","Chimbarongo","Nancagua","Placilla","Santa Cruz","Palmilla","Peralillo",
        "Lolol","Pumanque",
        "Pichilemu","La Estrella","Litueche","Marchigüe","Navidad"
    ],
    "Maule": [
        "Talca","San Clemente","Pelarco","Río Claro","Pencahue","Maule","Curepto","Constitución",
        "Curicó","Teno","Romeral","Rauco","Sagrada Familia","Molina","Hualañé","Licantén","Vichuquén",
        "Linares","Yerbas Buenas","Colbún","Longaví","Retiro","Parral",
        "Cauquenes","Pelluhue","Chanco",
        "San Javier","Villa Alegre"
    ],
    "Ñuble": [
        "Chillán","Chillán Viejo","Quillón","Bulnes","San Ignacio","El Carmen","Pemuco","Yungay",
        "Pinto","Coihueco","San Nicolás","San Carlos","Ñiquén","Coelemu","Ránquil","Portezuelo",
        "Ninhue","Quirihue","Cobquecura","Trehuaco"
    ],
    "Biobío": [
        # Concepción
        "Concepción","Talcahuano","Hualpén","San Pedro de la Paz","Chiguayante","Penco","Tomé",
        "Florida","Hualqui","Coronel","Lota","Santa Juana",
        # Biobío
        "Los Ángeles","Mulchén","Nacimiento","Negrete","Laja","San Rosendo","Yumbel","Cabrero",
        "Quilleco","Quilaco","Santa Bárbara","Alto Biobío",
        # Arauco
        "Arauco","Cañete","Contulmo","Curanilahue","Lebu","Los Álamos","Tirúa"
    ],
    "La Araucanía": [
        # Cautín
        "Temuco","Padre Las Casas","Lautaro","Perquenco","Vilcún","Cunco","Melipeuco",
        "Curarrehue","Pucón","Villarrica","Freire","Gorbea","Loncoche","Toltén","Saavedra",
        "Teodoro Schmidt","Carahue","Nueva Imperial","Cholchol",
        # Malleco
        "Angol","Renaico","Collipulli","Ercilla","Traiguén","Lumaco","Purén","Los Sauces"
    ],
    "Los Ríos": [
        "Valdivia","Corral","Lanco","Máfil","Mariquina","Paillaco","Panguipulli",
        "La Unión","Río Bueno","Futrono","Lago Ranco"
    ],
    "Los Lagos": [
        # Llanquihue
        "Puerto Montt","Puerto Varas","Llanquihue","Frutillar","Fresia","Maullín","Calbuco","Cochamó",
        # Osorno
        "Osorno","San Pablo","San Juan de la Costa","Puyehue","Río Negro","Purranque",
        # Chiloé
        "Castro","Chonchi","Curaco de Vélez","Dalcahue","Puqueldón","Queilén","Quellón","Quemchi","Ancud","Quinchao",
        # Palena
        "Chaitén","Futaleufú","Hualaihué","Palena"
    ],
    "Aysén": [
        "Coyhaique","Lago Verde","Aysén","Cisnes","Guaitecas",
        "Cochrane","O’Higgins","Tortel","Chile Chico","Río Ibáñez"
    ],
    "Magallanes": [
        "Punta Arenas","Laguna Blanca","Río Verde","San Gregorio",
        "Natales","Torres del Paine",
        "Porvenir","Primavera","Timaukel",
        "Cabo de Hornos","Antártica"
    ],
}

def region_slug(name: str) -> str:
    """Slug estable para usar en URL (maneja apóstrofos/ñ)."""
    return dj_slugify(name).replace("-", "_")

ALL_COMUNAS_CHOICES = [(c, c) for r in COMUNAS_POR_REGION.values() for c in r]
