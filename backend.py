# backend.py
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # CORS hatası olmaması için

# API Endpoint'leri
API_ENDPOINTS = {
    # Plaka İşlemleri
    "plaka_sorgu": "https://plakanabi.onrender.com/plaka?plaka={plaka}",
    "plaka_ad": "https://plakanabi.onrender.com/plaka-ad?ad={ad}",
    "plaka_soyad": "https://plakanabi.onrender.com/plaka-soyad?soyad={soyad}",
    "plaka_adsoyad": "https://plakanabi.onrender.com/plaka-adsoyad?ad={ad}&soyad={soyad}",
    "plaka_text": "https://apinabi.onrender.com/plaka/text?plaka={plaka}",
    
    # Papara İşlemleri
    "papara_no": "https://papara.onrender.com/paparano?paparano={paparano}",
    "papara_ad": "https://papara.onrender.com/ad?ad={ad}",
    "papara_soyad": "https://papara.onrender.com/soyad?soyad={soyad}",
    "papara_adsoyad": "https://papara.onrender.com/adsoyad?ad={ad}&soyad={soyad}",
    
    # TC Kimlik İşlemleri
    "tc_sorgu1": "https://apinabi.onrender.com/tc/text?tc={tc}",
    "tc_sorgu2": "https://apinabi.onrender.com/tc2/text?tc={tc}",
    
    # GSM İşlemleri
    "gsm_sorgu1": "https://apinabi.onrender.com/gsm/text?gsm={gsm}",
    "gsm_sorgu2": "https://apinabi.onrender.com/gsm2/text?gsm={gsm}",
    
    # Aile ve Hane İşlemleri
    "aile_sorgu": "https://apinabi.onrender.com/aile/text?tc={tc}",
    "sulale_sorgu": "https://apinabi.onrender.com/sulale/text?tc={tc}",
    "hane_sorgu": "https://apinabi.onrender.com/hane/text?tc={tc}",
    
    # İş Yeri ve Vesika İşlemleri
    "isyeri_sorgu": "https://apinabi.onrender.com/isyeri/text?tc={tc}",
    "vesika_sorgu": "https://apinabi.onrender.com/vesika/text?tc={tc}",
    
    # Ad-Soyad İşlemleri
    "adsoyad_sorgu": "https://apinabi.onrender.com/text?name={name}&surname={surname}",
    "sicil_ad": "https://siciln.onrender.com/ad?ad={ad}",
    "sicil_soyad": "https://siciln.onrender.com/soyad?soyad={soyad}",
    "sicil_adsoyad": "https://siciln.onrender.com/adsoyad?ad={ad}&soyad={soyad}",
    
    # Sicil / ID İşlemleri
    "sicil_id": "https://siciln.onrender.com/id?id={id}",
    
    # Nüfus ve Resmi Kurum İşlemleri
    "nufus_sorgu": "https://panel-w6tk.onrender.com/api/v1/nufus/sorgu?tc={tc}",
    "adli_sicil": "https://panel-w6tk.onrender.com/api/v1/adli-sicil/kayit?tc={tc}",
    "pasaport_sorgu": "https://panel-w6tk.onrender.com/api/v1/pasaport/sorgu?tc={tc}",
    "ehliyet_sorgu": "https://panel-w6tk.onrender.com/api/v1/ehliyet/sorgu?tc={tc}",
    "meb_mezuniyet": "https://panel-w6tk.onrender.com/api/v1/meb/mezuniyet?tc={tc}",
    "noter_islem": "https://panel-w6tk.onrender.com/api/v1/noter/gereceklesen-islem?tc={tc}",
    
    # Sağlık İşlemleri
    "asi_kayitlari": "https://panel-w6tk.onrender.com/api/v1/saglik/asi-kayitlari?tc={tc}",
    "rontgen_listesi": "https://panel-w6tk.onrender.com/api/v1/saglik/rontgen-listesi?tc={tc}",
    "kronik_hastalik": "https://panel-w6tk.onrender.com/api/v1/saglik/kronik-hastalik?tc={tc}",
    "hasta_yatis": "https://panel-w6tk.onrender.com/api/v1/saglik/hasta-yatis-gecmisi?tc={tc}",
    "recete_gecmisi": "https://panel-w6tk.onrender.com/api/v1/eczane/recete-gecmisi?tc={tc}",
    
    # Vergi ve Ticaret İşlemleri
    "vergi_borc": "https://panel-w6tk.onrender.com/api/v1/vergi/borc-sorgu?tc={tc}",
    "ticaret_sikayet": "https://panel-w6tk.onrender.com/api/v1/ticaret/sikayet-kaydi?tc={tc}",
    
    # Tapu ve Gayrimenkul İşlemleri
    "gayrimenkul": "https://panel-w6tk.onrender.com/api/v1/tapu/gayrimenkul?tc={tc}",
    
    # Askerlik İşlemleri
    "askerlik_durum": "https://panel-w6tk.onrender.com/api/v1/askerlik/durum?tc={tc}",
    
    # Fatura İşlemleri
    "ibb_su": "https://panel-w6tk.onrender.com/api/v1/ibb/su-fatura?tc={tc}",
    "elektrik_fatura": "https://panel-w6tk.onrender.com/api/v1/elektrik/fatura?tc={tc}",
    
    # Turizm ve Ulaşım İşlemleri
    "otel_rezervasyon": "https://panel-w6tk.onrender.com/api/v1/turizm/otel-rezervasyon?tc={tc}",
    "istanbulkart_bakiye": "https://panel-w6tk.onrender.com/api/v1/ulasim/istanbulkart-bakiye?tc={tc}",
    "ucak_bilet": "https://panel-w6tk.onrender.com/api/v1/udhb/ucak-bilet?tc={tc}",
    "seyahat_hareket": "https://panel-w6tk.onrender.com/api/v1/mzk/seyahat-hareket?tc={tc}",
    
    # Spor ve Kültür İşlemleri
    "spor_federasyon": "https://panel-w6tk.onrender.com/api/v1/spor/federasyon/kayit?tc={tc}",
    "kutuphane_uye": "https://panel-w6tk.onrender.com/api/v1/kutuphane/uye-durum?tc={tc}",
    
    # Banka ve Kredi İşlemleri
    "dijital_banka": "https://panel-w6tk.onrender.com/api/v1/dijital/banka-musteri?tc={tc}",
    "kredi_risk": "https://panel-w6tk.onrender.com/api/v1/kredi/risk-raporu?tc={tc}",
    
    # Çevre ve Doğa İşlemleri
    "cevre_ceza": "https://panel-w6tk.onrender.com/api/v1/cevre/sehirlerarasi-ceza?tc={tc}",
    "avci_lisans": "https://panel-w6tk.onrender.com/api/v1/ormancilik/avci-lisans?tc={tc}"
}

# Sorgu adlarını tutan mapping
QUERY_NAMES = {
    # Plaka İşlemleri
    "Plaka Sorgu": "plaka_sorgu",
    "Plaka Ad Sorgu": "plaka_ad",
    "Plaka Soyad Sorgu": "plaka_soyad",
    "Plaka Ad-Soyad Sorgu": "plaka_adsoyad",
    "Plaka Text Sorgu": "plaka_text",
    
    # Papara İşlemleri
    "Papara No Sorgu": "papara_no",
    "Papara Ad Sorgu": "papara_ad",
    "Papara Soyad Sorgu": "papara_soyad",
    "Papara Ad-Soyad Sorgu": "papara_adsoyad",
    
    # TC Kimlik İşlemleri
    "TC Sorgu 1": "tc_sorgu1",
    "TC Sorgu 2": "tc_sorgu2",
    
    # GSM İşlemleri
    "GSM Sorgu 1": "gsm_sorgu1",
    "GSM Sorgu 2": "gsm_sorgu2",
    
    # Aile ve Hane İşlemleri
    "Aile Sorgu": "aile_sorgu",
    "Sülale Sorgu": "sulale_sorgu",
    "Hane Sorgu": "hane_sorgu",
    
    # İş Yeri ve Vesika İşlemleri
    "İş Yeri Sorgu": "isyeri_sorgu",
    "Vesika Sorgu": "vesika_sorgu",
    
    # Ad-Soyad İşlemleri
    "Ad-Soyad Sorgu": "adsoyad_sorgu",
    "Sicil Ad Sorgu": "sicil_ad",
    "Sicil Soyad Sorgu": "sicil_soyad",
    "Sicil Ad-Soyad Sorgu": "sicil_adsoyad",
    
    # Sicil / ID İşlemleri
    "Sicil ID Sorgu": "sicil_id",
    
    # Nüfus ve Resmi Kurum İşlemleri
    "Nüfus Sorgu": "nufus_sorgu",
    "Adli Sicil Kayıt": "adli_sicil",
    "Pasaport Sorgu": "pasaport_sorgu",
    "Ehliyet Sorgu": "ehliyet_sorgu",
    "MEB Mezuniyet": "meb_mezuniyet",
    "Noter İşlem": "noter_islem",
    
    # Sağlık İşlemleri
    "Aşı Kayıtları": "asi_kayitlari",
    "Röntgen Listesi": "rontgen_listesi",
    "Kronik Hastalık": "kronik_hastalik",
    "Hasta Yatış Geçmişi": "hasta_yatis",
    "Reçete Geçmişi": "recete_gecmisi",
    
    # Vergi ve Ticaret İşlemleri
    "Vergi Borç Sorgu": "vergi_borc",
    "Ticaret Şikayet Kaydı": "ticaret_sikayet",
    
    # Tapu ve Gayrimenkul İşlemleri
    "Gayrimenkul Sorgu": "gayrimenkul",
    
    # Askerlik İşlemleri
    "Askerlik Durum": "askerlik_durum",
    
    # Fatura İşlemleri
    "İBB Su Fatura": "ibb_su",
    "Elektrik Fatura": "elektrik_fatura",
    
    # Turizm ve Ulaşım İşlemleri
    "Otel Rezervasyon": "otel_rezervasyon",
    "İstanbulkart Bakiye": "istanbulkart_bakiye",
    "Uçak Bilet": "ucak_bilet",
    "Seyahat Hareket": "seyahat_hareket",
    
    # Spor ve Kültür İşlemleri
    "Spor Federasyon Kayıt": "spor_federasyon",
    "Kütüphane Üye Durum": "kutuphane_uye",
    
    # Banka ve Kredi İşlemleri
    "Dijital Banka Müşteri": "dijital_banka",
    "Kredi Risk Raporu": "kredi_risk",
    
    # Çevre ve Doğa İşlemleri
    "Şehirlerarası Çevre Ceza": "cevre_ceza",
    "Avcı Lisans": "avci_lisans"
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/query/<query_name>')
def query_page(query_name):
    """Sorgu sayfasını render eder"""
    if query_name not in QUERY_NAMES.values():
        return "Geçersiz sorgu!", 404
    
    # Sorgu adını bul
    display_name = [k for k, v in QUERY_NAMES.items() if v == query_name][0]
    
    return render_template('query.html', 
                         query_name=display_name,
                         query_key=query_name)

@app.route('/api/execute_query', methods=['POST'])
def execute_query():
    """Sorguyu çalıştırır ve sonucu döndürür"""
    try:
        data = request.json
        query_key = data.get('query_key')
        params = data.get('params', {})
        
        if query_key not in API_ENDPOINTS:
            return jsonify({"error": "Geçersiz sorgu anahtarı"}), 400
        
        # API endpoint'ini al
        api_url = API_ENDPOINTS[query_key]
        
        # Parametreleri URL'ye ekle
        for key, value in params.items():
            api_url = api_url.replace(f"{{{key}}}", str(value))
        
        # API'yi çağır
        response = requests.get(api_url, timeout=30)
        
        # JSON response döndür
        return jsonify({
            "success": True,
            "api_url": api_url,
            "status_code": response.status_code,
            "response": response.text
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/get_query_info/<query_key>')
def get_query_info(query_key):
    """Sorgu için gerekli parametreleri döndürür"""
    if query_key not in API_ENDPOINTS:
        return jsonify({"error": "Geçersiz sorgu anahtarı"}), 404
    
    api_url = API_ENDPOINTS[query_key]
    
    # URL'den parametreleri çıkar
    import re
    params = re.findall(r'\{(.*?)\}', api_url)
    
    return jsonify({
        "query_key": query_key,
        "api_url_template": api_url,
        "required_params": params
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
