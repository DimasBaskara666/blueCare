from typing import Dict, List, Any, Optional
import re
import logging

logger = logging.getLogger(__name__)

class HealthAssistant:
    def __init__(self):
        # Expanded patterns and synonyms for symptoms and intents
        self.symptom_synonyms = {
            "demam": ["demam", "panas", "suhu tinggi", "meriang"],
            "sakit_kepala": ["sakit kepala", "pusing", "kepala nyeri", "migren"],
            "batuk": ["batuk", "batuk kering", "batuk berdahak"],
            "pilek": ["pilek", "hidung meler", "flu ringan"],
            "nyeri_otot": ["nyeri otot", "pegal", "otot sakit"],
            "ruam": ["ruam", "bintik merah", "kulit merah"],
            "mual": ["mual", "ingin muntah", "loya"],
            "muntah": ["muntah", "keluar muntah"],
            "sakit_perut": ["sakit perut", "perut nyeri", "perut mulas"],
            "perut_kembung": ["perut kembung", "perut begah"],
            "pusing": ["pusing", "kepala ringan", "kepala berputar"],
            "lemas": ["lemas", "letih", "kurang tenaga"],
            "sering_haus": ["sering haus", "haus terus", "banyak minum"],
            "sering_kencing": ["sering kencing", "kencing terus", "buang air kecil sering"],
            "sesak_nafas": ["sesak nafas", "sulit bernafas", "nafas pendek", "nafas berat"],
            "dada_sesak": ["dada sesak", "dada berat", "nyeri dada"],
            "dbd": ["dbd", "demam berdarah", "demam dengue"],
            "tipes": ["tipes", "tifus", "demam tifoid"],
            "ispa": ["ispa", "infeksi saluran pernapasan akut", "batuk pilek"],
            "maag": ["maag", "gastritis", "sakit lambung"],
            "diare": ["diare", "mencret", "buang air besar cair"]
        }

        # Expanded QA pairs and advice
        self.qa_pairs = {
            r"halo|hai|hi|hello|hei": "Halo! Saya asisten kesehatan Anda. Apa yang bisa saya bantu?",
            r"apa kabar|bagaimana kabar": "Saya baik, terima kasih! Bagaimana dengan Anda?",
            r"terima kasih|makasih": "Sama-sama! Ada yang bisa saya bantu lagi?",
            r"bagaimana cara mengatasi demam": "Untuk mengatasi demam, Anda bisa: istirahat, minum air putih, kompres hangat, dan minum obat penurun demam jika perlu.",
            r"apa gejala covid|covid-19|corona": "Gejala umum COVID-19: demam, batuk kering, kelelahan, kehilangan penciuman/perasa, sesak nafas, sakit tenggorokan, nyeri otot.",
            r"kapan harus ke dokter": "Segera ke dokter jika mengalami: sesak nafas parah, nyeri dada, kejang, pingsan, demam tinggi yang tidak turun, atau gejala memburuk.",
            r"apa gejala dbd|demam berdarah": "Gejala DBD: demam tinggi mendadak, nyeri otot, ruam, perdarahan ringan (mimisan, gusi berdarah). Segera ke dokter jika ada tanda perdarahan atau syok.",
            r"apa gejala tipes|tifus": "Gejala tipes: demam bertahap, sakit kepala, lemas, nyeri perut, konstipasi atau diare. Segera ke dokter jika demam berkelanjutan.",
            r"apa gejala ispa|infeksi saluran pernapasan": "Gejala ISPA: batuk, pilek, sakit tenggorokan, demam ringan. Istirahat dan minum air hangat. Segera ke dokter jika sesak nafas atau demam tinggi.",
            r"apa gejala maag|gastritis": "Gejala maag: nyeri ulu hati, mual, kembung, muntah. Hindari makanan pedas/berlemak. Segera ke dokter jika nyeri hebat atau muntah darah.",
            r"apa gejala diare|mencret": "Gejala diare: buang air besar cair, nyeri perut, dehidrasi. Minum oralit, hindari makanan berminyak. Segera ke dokter jika dehidrasi berat atau diare berdarah."
        }

        self.symptom_questions = {
            "demam": [
                "Berapa suhu tubuh Anda?",
                "Apakah demam disertai menggigil?",
                "Sudah berapa lama demam berlangsung?",
                "Apakah ada gejala lain yang menyertai?"
            ],
            "sakit_kepala": [
                "Di bagian mana kepala terasa sakit?",
                "Apakah sakit kepala terasa berdenyut?",
                "Apakah ada gejala lain yang menyertai?",
                "Apakah sakit kepala muncul tiba-tiba atau bertahap?"
            ],
            "batuk": [
                "Apakah batuk berdahak?",
                "Sudah berapa lama batuk berlangsung?",
                "Apakah batuk lebih parah di malam hari?",
                "Apakah ada darah dalam dahak?"
            ],
            "mual": [
                "Apakah disertai muntah?",
                "Kapan terakhir kali makan?",
                "Apakah ada makanan yang baru dikonsumsi?",
                "Apakah mual disertai nyeri perut?"
            ],
            "sering_kencing": [
                "Berapa kali Anda buang air kecil dalam sehari?",
                "Apakah disertai rasa nyeri atau panas?",
                "Apakah urine berwarna keruh atau berdarah?",
                "Apakah Anda merasa haus berlebihan?"
            ],
            "sesak_nafas": [
                "Apakah sesak nafas muncul tiba-tiba?",
                "Apakah ada riwayat asma?",
                "Apakah sesak nafas memburuk saat aktivitas?",
                "Apakah disertai batuk atau demam?"
            ],
            "lemas": [
                "Sejak kapan Anda merasa lemas?",
                "Apakah lemas disertai pusing atau mual?",
                "Apakah Anda cukup makan dan minum?"
            ],
            "dbd": [
                "Apakah demam tinggi mendadak?",
                "Apakah ada ruam atau perdarahan?",
                "Apakah ada nyeri otot atau sendi?",
                "Apakah ada riwayat gigitan nyamuk?"
            ],
            "tipes": [
                "Apakah demam bertahap?",
                "Apakah ada sakit kepala atau lemas?",
                "Apakah ada nyeri perut?",
                "Apakah ada riwayat konsumsi makanan/minuman terkontaminasi?"
            ],
            "ispa": [
                "Apakah ada batuk atau pilek?",
                "Apakah ada sakit tenggorokan?",
                "Apakah ada demam?",
                "Apakah ada riwayat kontak dengan penderita ISPA?"
            ],
            "maag": [
                "Apakah ada nyeri ulu hati?",
                "Apakah ada mual atau kembung?",
                "Apakah ada muntah?",
                "Apakah ada riwayat konsumsi makanan pedas/berlemak?"
            ],
            "diare": [
                "Berapa kali buang air besar dalam sehari?",
                "Apakah ada nyeri perut?",
                "Apakah ada dehidrasi (mulut kering, lemas)?",
                "Apakah ada riwayat konsumsi makanan/minuman terkontaminasi?"
            ]
        }

        self.health_advice = {
            "demam": "Untuk demam: istirahat, minum air putih, kompres hangat, minum obat penurun demam jika suhu di atas 38°C. Segera ke dokter jika demam di atas 39°C atau lebih dari 3 hari.",
            "batuk": "Untuk batuk: minum air hangat, hindari makanan/minuman dingin, gunakan masker, istirahat cukup. Segera ke dokter jika batuk berdarah atau lebih dari 2 minggu.",
            "mual": "Untuk mual: makan porsi kecil tapi sering, hindari makanan berlemak/pedas, minum air jahe hangat, istirahat cukup. Segera ke dokter jika muntah terus-menerus atau berdarah.",
            "sering_kencing": "Untuk sering kencing: batasi kafein/alkohol, minum air secukupnya, latihan otot panggul, jaga kebersihan. Segera ke dokter jika disertai nyeri, urine berdarah, atau demam.",
            "sesak_nafas": "Untuk sesak nafas: duduk tegak, tarik nafas perlahan, hindari aktivitas berat, jauhi pemicu alergi. Segera ke dokter jika sesak parah, bibir membiru, nyeri dada, atau kesadaran menurun.",
            "lemas": "Untuk lemas: cukup istirahat, makan makanan bergizi, minum air putih. Segera ke dokter jika lemas berat, tidak membaik, atau disertai gejala lain.",
            "dbd": "Untuk DBD: istirahat total, minum air putih, hindari obat antiinflamasi, segera ke dokter jika ada perdarahan atau syok.",
            "tipes": "Untuk tipes: istirahat, makan makanan lunak, minum air putih, hindari makanan pedas/berlemak. Segera ke dokter jika demam berkelanjutan atau ada komplikasi.",
            "ispa": "Untuk ISPA: istirahat, minum air hangat, gunakan masker, hindari rokok. Segera ke dokter jika sesak nafas atau demam tinggi.",
            "maag": "Untuk maag: makan teratur, hindari makanan pedas/berlemak, hindari rokok/alkohol, minum obat maag jika perlu. Segera ke dokter jika nyeri hebat atau muntah darah.",
            "diare": "Untuk diare: minum oralit, hindari makanan berminyak, istirahat cukup. Segera ke dokter jika dehidrasi berat atau diare berdarah."
        }

    def _normalize_symptoms(self, text: str) -> List[str]:
        """Extract normalized symptom keys from user text using synonyms."""
        found = set()
        text = text.lower()
        for key, synonyms in self.symptom_synonyms.items():
            for syn in synonyms:
                if syn in text:
                    found.add(key)
        return list(found)

    def _get_qa_response(self, text: str) -> Optional[str]:
        text = text.lower()
        for pattern, response in self.qa_pairs.items():
            if re.search(pattern, text):
                return response
        return None

    def _get_symptom_questions(self, medical_terms: List[str]) -> List[str]:
        questions = []
        for term in medical_terms:
            if term in self.symptom_questions:
                questions.extend(self.symptom_questions[term])
        return list(set(questions))

    def _get_health_advice(self, medical_terms: List[str]) -> List[str]:
        advice = []
        for term in medical_terms:
            if term in self.health_advice:
                advice.append(self.health_advice[term])
        return advice

    def get_response(self, text: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        if context is None:
            context = {}

        # Normalize symptoms from user text
        normalized_symptoms = self._normalize_symptoms(text)
        medical_terms = context.get("medical_terms", [])
        all_terms = list(set(normalized_symptoms + medical_terms))

        # Check for general questions first
        qa_response = self._get_qa_response(text)
        if qa_response:
            return {
                "response": qa_response,
                "suggestions": [
                    "Apakah ada gejala lain yang ingin Anda tanyakan?",
                    "Apakah Anda ingin informasi lebih lanjut?",
                    "Apakah ada hal lain yang bisa saya bantu?"
                ],
                "context": {"medical_terms": all_terms}
            }

        # Get follow-up questions
        questions = self._get_symptom_questions(all_terms)
        advice = self._get_health_advice(all_terms)

        response_parts = []
        if questions:
            response_parts.append("Untuk membantu diagnosis lebih akurat, mohon jawab beberapa pertanyaan:")
            for i, question in enumerate(questions[:3], 1):
                response_parts.append(f"{i}. {question}")
        if advice:
            response_parts.append("\nBeberapa saran kesehatan:")
            response_parts.extend(advice)
        if not response_parts:
            response_parts.append("Mohon jelaskan gejala yang Anda alami lebih detail. Beberapa hal yang perlu dijelaskan:\n1. Gejala utama yang Anda rasakan\n2. Kapan gejala mulai muncul\n3. Apakah ada gejala lain yang menyertai\n4. Apakah ada riwayat penyakit sebelumnya")

        return {
            "response": "\n".join(response_parts),
            "suggestions": [
                "Apakah ada gejala lain?",
                "Sudah berapa lama gejala ini berlangsung?",
                "Apakah ada riwayat penyakit sebelumnya?",
                "Apakah ada obat yang sedang dikonsumsi?"
            ],
            "context": {"medical_terms": all_terms}
        }

# Global chatbot instance
_chatbot = None

def initialize_chatbot():
    global _chatbot
    if _chatbot is None:
        _chatbot = HealthAssistant()

def get_chatbot_response(text: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
    global _chatbot
    if _chatbot is None:
        initialize_chatbot()
    return _chatbot.get_response(text, context) 