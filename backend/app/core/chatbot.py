from typing import Dict, List, Any
import re
import logging

logger = logging.getLogger(__name__)

class HealthAssistant:
    def __init__(self):
        # Common questions and responses
        self.qa_pairs = {
            r"halo|hai|hi|hello|hei": "Halo! Saya asisten kesehatan Anda. Apa yang bisa saya bantu?",
            r"apa kabar|bagaimana kabar": "Saya baik, terima kasih! Bagaimana dengan Anda?",
            r"terima kasih|makasih": "Sama-sama! Ada yang bisa saya bantu lagi?",
            r"bagaimana cara mengatasi demam": "Untuk mengatasi demam, Anda bisa:\n1. Istirahat yang cukup\n2. Minum banyak air putih (minimal 8 gelas per hari)\n3. Kompres dengan air hangat\n4. Minum obat penurun demam jika suhu di atas 38°C\n5. Gunakan pakaian yang nyaman dan tidak terlalu tebal\n\nSegera ke dokter jika:\n- Demam di atas 39°C\n- Demam berlangsung lebih dari 3 hari\n- Disertai gejala lain seperti sesak nafas atau kejang",
            r"apa gejala covid|covid-19|corona": "Gejala umum COVID-19 meliputi:\n1. Demam (suhu di atas 37.5°C)\n2. Batuk kering\n3. Kelelahan\n4. Kehilangan indra penciuman atau perasa\n5. Sesak nafas\n6. Sakit tenggorokan\n7. Nyeri otot\n\nGejala serius yang memerlukan perhatian medis segera:\n- Kesulitan bernafas\n- Nyeri atau tekanan di dada\n- Kebingungan\n- Ketidakmampuan untuk bangun atau tetap terjaga\n- Warna kebiruan pada bibir atau wajah\n\nJika mengalami gejala-gejala tersebut, segera hubungi fasilitas kesehatan terdekat.",
            r"kapan harus ke dokter": "Anda harus segera ke dokter jika mengalami:\n\n1. Gejala Darurat:\n- Sesak nafas parah\n- Nyeri dada\n- Kejang\n- Pingsan\n- Perdarahan hebat\n\n2. Gejala Serius:\n- Demam tinggi (>39°C) yang tidak turun\n- Sakit kepala parah dan tiba-tiba\n- Muntah terus-menerus\n- Diare parah\n- Ruam kulit yang menyebar cepat\n\n3. Kondisi Kronis:\n- Gejala yang berlangsung lebih dari 1 minggu\n- Gejala yang semakin memburuk\n- Gejala yang mengganggu aktivitas sehari-hari\n\n4. Pasca Operasi/Kecelakaan:\n- Demam\n- Nyeri yang meningkat\n- Luka yang tidak sembuh\n- Tanda-tanda infeksi (kemerahan, bengkak, nanah)"
        }
        
        # Follow-up questions for symptoms
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
            ]
        }
        
        # General health advice
        self.health_advice = {
            "demam": "Untuk demam:\n1. Istirahat yang cukup\n2. Minum banyak air putih\n3. Kompres dengan air hangat\n4. Minum obat penurun demam jika suhu di atas 38°C\n\nSegera ke dokter jika:\n- Demam di atas 39°C\n- Demam berlangsung lebih dari 3 hari\n- Disertai gejala lain seperti sesak nafas atau kejang",
            "batuk": "Untuk batuk:\n1. Minum air hangat dengan madu\n2. Hindari makanan/minuman dingin\n3. Gunakan masker jika keluar rumah\n4. Istirahat yang cukup\n5. Hindari merokok dan asap rokok\n\nSegera ke dokter jika:\n- Batuk berdarah\n- Batuk berlangsung lebih dari 2 minggu\n- Disertai demam tinggi",
            "mual": "Untuk mual:\n1. Makan dalam porsi kecil tapi sering\n2. Hindari makanan berlemak dan pedas\n3. Minum air jahe hangat\n4. Istirahat yang cukup\n5. Hindari berbaring setelah makan\n\nSegera ke dokter jika:\n- Muntah terus-menerus\n- Muntah berdarah\n- Disertai nyeri perut hebat",
            "sering_kencing": "Untuk sering kencing:\n1. Batasi konsumsi kafein dan alkohol\n2. Minum air putih secukupnya\n3. Latihan otot dasar panggul\n4. Jaga kebersihan area kencing\n\nSegera ke dokter jika:\n- Disertai nyeri atau panas saat kencing\n- Urine berdarah atau keruh\n- Demam\n- Nyeri pinggang",
            "sesak_nafas": "Untuk sesak nafas:\n1. Duduk dengan posisi tegak\n2. Tarik nafas perlahan dan dalam\n3. Hindari aktivitas berat\n4. Jauhi pemicu alergi\n\nSegera ke dokter jika:\n- Sesak nafas parah\n- Bibir atau kuku membiru\n- Nyeri dada\n- Kesadaran menurun"
        }

    def _get_qa_response(self, text: str) -> str:
        """Get response for general questions"""
        text = text.lower()
        for pattern, response in self.qa_pairs.items():
            if re.search(pattern, text):
                return response
        return None

    def _get_symptom_questions(self, medical_terms: List[str]) -> List[str]:
        """Get relevant follow-up questions for symptoms"""
        questions = []
        for term in medical_terms:
            if term in self.symptom_questions:
                questions.extend(self.symptom_questions[term])
        return list(set(questions))  # Remove duplicates

    def _get_health_advice(self, medical_terms: List[str]) -> List[str]:
        """Get health advice for symptoms"""
        advice = []
        for term in medical_terms:
            if term in self.health_advice:
                advice.append(self.health_advice[term])
        return advice

    def get_response(self, text: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Get chatbot response based on input text and context"""
        if context is None:
            context = {}
        
        # Check for general questions first
        qa_response = self._get_qa_response(text)
        if qa_response:
            return {
                "response": qa_response,
                "suggestions": [
                    "Apakah ada gejala lain yang ingin Anda tanyakan?",
                    "Apakah Anda ingin informasi lebih lanjut?",
                    "Apakah ada hal lain yang bisa saya bantu?"
                ]
            }
        
        # Process medical terms from context
        medical_terms = context.get("medical_terms", [])
        
        # Get follow-up questions
        questions = self._get_symptom_questions(medical_terms)
        
        # Get health advice
        advice = self._get_health_advice(medical_terms)
        
        # Construct response
        response_parts = []
        
        if questions:
            response_parts.append("Untuk membantu diagnosis lebih akurat, mohon jawab beberapa pertanyaan:")
            for i, question in enumerate(questions[:3], 1):  # Limit to 3 most relevant questions
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
            ]
        }

# Global chatbot instance
_chatbot = None

def initialize_chatbot():
    """Initialize the global chatbot"""
    global _chatbot
    if _chatbot is None:
        _chatbot = HealthAssistant()

def get_chatbot_response(text: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
    """Get response from the global chatbot"""
    global _chatbot
    if _chatbot is None:
        initialize_chatbot()
    
    return _chatbot.get_response(text, context) 