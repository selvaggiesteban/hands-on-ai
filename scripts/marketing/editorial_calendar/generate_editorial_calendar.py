import csv
import os
import random
from datetime import date, timedelta

# Configuration
START_DATE = date(2026, 1, 26)
END_DATE = date(2026, 12, 31)
OUTPUT_FILE = "calendario_editorial_2026.csv"

VERTICALS = [
    "Clínica Dermatológica",
    "Clínica Dental",
    "Clínica de Nutrición",
    "Coach Personal",
    "Empresa de Construcción"
]

PLATFORMS = [
    "lanuscomputacion.com",
    "Facebook",
    "Instagram",
    "TikTok",
    "LinkedIn",
    "Reddit",
    "Medium"
]

# Templates for content generation to ensure variety
TEMPLATES = {
    "Clínica Dermatológica": {
        "keywords": ["tratamiento acne", "rejuvenecimiento facial", "dermatologia estetica", "cuidado de la piel", "laser co2"],
        "prompts_img": "Professional dermatology clinic, modern equipment, doctor consulting patient, bright lighting, photorealistic, 8k",
        "prompts_vid": "Slow motion shot of laser treatment application, close up on healthy skin texture, professional dermatologist smiling",
        "topics": ["Cómo cuidar tu piel en verano", "Tratamientos revolucionarios para el acné", "La importancia de la hidratación facial"]
    },
    "Clínica Dental": {
        "keywords": ["implantes dentales", "blanqueamiento dental", "ortodoncia invisible", "carillas de porcelana", "salud bucal"],
        "prompts_img": "Modern dental office, dentist checking x-ray, smiling patient with perfect teeth, clean white aesthetic, 8k",
        "prompts_vid": "Time lapse of dental cleaning procedure, 3d animation of dental implant, happy family at dentist reception",
        "topics": ["Sonrisa perfecta en 3 pasos", "Mitos sobre el blanqueamiento dental", "Implantes vs Prótesis: ¿Qué elegir?"]
    },
    "Clínica de Nutrición": {
        "keywords": ["plan alimenticio personalizado", "nutricion deportiva", "bajar de peso saludablemente", "dietas keto", "nutricionista online"],
        "prompts_img": "Fresh healthy food bowl, nutritionist measuring patient, meal prep containers, vibrant colors, wellness concept, 8k",
        "prompts_vid": "Chef preparing healthy salad, nutritionist explaining food pyramid, person jogging in park morning light",
        "topics": ["Nutrición para deportistas de alto rendimiento", "Cómo leer etiquetas nutricionales", "Recetas saludables para la oficina"]
    },
    "Coach Personal": {
        "keywords": ["liderazgo personal", "gestion del tiempo", "superacion personal", "coaching ejecutivo", "metas 2026"],
        "prompts_img": "Business coach speaking at seminar, confident person looking at city skyline, handshake close up, motivational atmosphere, 8k",
        "prompts_vid": "Coach giving speech with gestures, person climbing mountain peak drone shot, team brainstorming session time lapse",
        "topics": ["Desbloquea tu potencial máximo", "Gestión del tiempo para emprendedores", "Cómo establecer metas alcanzables"]
    },
    "Empresa de Construcción": {
        "keywords": ["reformas integrales", "construccion en seco", "arquitectura moderna", "presupuesto obra", "diseño de interiores"],
        "prompts_img": "Construction site with crane, architect reviewing blueprints, modern luxury house facade, golden hour, photorealistic, 8k",
        "prompts_vid": "Drone footage of building construction progress, timelapse of wall painting, worker placing bricks precision",
        "topics": ["Tendencias en construcción 2026", "Cómo calcular el costo de tu reforma", "Materiales sustentables para tu hogar"]
    }
}

CTA = "\n\nSolicitá tu presupuesto ahora. Comunicate por WhatsApp al +54 9 11 5332 3937 y visitanos en lanuscomputacion.com para llevar tu negocio al siguiente nivel."

def generate_text(vertical, topic, keyword):
    # Simulating a ~300 word text structure
    intro = f"En el mundo competitivo de {vertical}, es fundamental destacar. Hoy hablaremos sobre '{topic}', un tema clave para quienes buscan excelencia. La '{keyword}' se ha convertido en un pilar esencial para el crecimiento y la satisfacción del cliente.\n\n"
    
    body_p1 = "Primero, analicemos el contexto actual. Las tendencias indican que la personalización y la calidad del servicio son más valoradas que nunca. Implementar estrategias correctas no solo mejora la percepción de tu marca, sino que también optimiza los recursos operativos. Es un momento crucial para invertir en soluciones que realmente marquen la diferencia.\n\n"
    
    body_p2 = f"Además, integrar tecnología y enfoques modernos en {vertical} permite alcanzar resultados medibles en menos tiempo. No se trata solo de trabajar más duro, sino de trabajar de manera más inteligente. Nuestros clientes han reportado mejoras significativas al adoptar estas prácticas, logrando fidelizar a su audiencia de manera efectiva.\n\n"
    
    body_p3 = "Por otro lado, la consistencia es clave. Mantener una presencia activa y ofrecer valor constante construye autoridad en el mercado. Ya sea que estés comenzando o busques expandirte, entender estos fundamentos sobre la '{keyword}' te dará una ventaja competitiva sostenible a largo plazo.\n\n"
    
    body_p4 = "Finalmente, recuerda que cada paso cuenta. La planificación estratégica y la ejecución impecable son las que separan a los líderes del resto. No dejes pasar la oportunidad de transformar tu visión en realidad con las herramientas adecuadas y el asesoramiento experto.\n\n"
    
    return intro + body_p1 + body_p2 + body_p3 + body_p4 + CTA

def generate_html5(text):
    paragraphs = text.split("\n\n")
    html_parts = ["<article>"]
    for p in paragraphs:
        if p.strip():
            html_parts.append(f"  <p>{p.strip()}</p>")
    html_parts.append("</article>")
    return "\n".join(html_parts)

def main():
    with open(OUTPUT_FILE, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Header
        writer.writerow([
            "fecha", "backlink", "carrusel de fotos", "videos", "texto", "html5", 
            "estado", "dirección URL", "palabra clave principal", "negocio local", 
            "prompts fotos", "prompts videos"
        ])

        current_date = START_DATE
        delta = timedelta(days=1)
        
        vertical_cycle = 0
        
        while current_date <= END_DATE:
            # Cycle through verticals daily
            vertical_name = VERTICALS[vertical_cycle % len(VERTICALS)]
            vertical_data = TEMPLATES[vertical_name]
            vertical_cycle += 1
            
            # Select random elements for variety
            platform = random.choice(PLATFORMS)
            keyword = random.choice(vertical_data["keywords"])
            topic = random.choice(vertical_data["topics"])
            
            # Generate content
            text_content = generate_text(vertical_name, topic, keyword)
            html_content = generate_html5(text_content)
            
            # Paths (Placeholders as requested)
            base_path = r"C:\Users\Esteban Selvaggi\Desktop\hands-on-ai\assets"
            date_str = current_date.strftime("%Y-%m-%d")
            photo_path = f"{base_path}\images\{date_str}_{vertical_name.replace(' ', '_')}.jpg"
            video_path = f"{base_path}\videos\{date_str}_{vertical_name.replace(' ', '_')}.mp4"
            
            writer.writerow([
                current_date.strftime("%d/%m/%Y"), # fecha
                platform,                          # backlink
                photo_path,                        # carrusel de fotos
                video_path,                        # videos
                text_content,                      # texto
                html_content,                      # html5
                "",                                # estado (vacío)
                "",                                # dirección URL (vacío)
                keyword,                           # palabra clave principal
                vertical_name,                     # negocio local
                vertical_data["prompts_img"],      # prompts fotos
                vertical_data["prompts_vid"]       # prompts videos
            ])
            
            current_date += delta

    print(f"Archivo generado exitosamente: {os.path.abspath(OUTPUT_FILE)}")

if __name__ == "__main__":
    main()
