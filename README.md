## Python ile Yemek Listesi Uygulaması

Bu Python uygulaması, bir iş yerindeki çalışanların yemek harcamalarını takip etmek için tasarlanmıştır. Tkinter kütüphanesi kullanarak kullanıcı arayüzü oluşturulmuş ve SQLite veritabanı ile veri saklama işlemleri gerçekleştirilmiştir.

### Kütüphaneler


#### Kütüphanelerin Rolü
* tkinter: Python'ın standart grafik kullanıcı arayüzü (GUI) kütüphanesidir. Bu uygulamada pencereler, düğmeler, giriş kutuları gibi tüm görsel öğeleri oluşturmak için kullanılır.
* ttk: Tkinter'ın temalı widget'larını içeren bir modüldür. Daha modern ve özelleştirilebilir kullanıcı arayüzleri oluşturmak için kullanılır.
* messagebox: Kullanıcıya mesaj kutuları (bilgi, uyarı, hata vb.) göstermek için kullanılır.
* colorchooser: Kullanıcının renk seçmesini sağlayan bir iletişim kutusu açar. Bu uygulamada, arayüzün renklerini özelleştirmek için kullanılabilir.
* simpledialog: Basit iletişim kutuları oluşturmak için kullanılır. Örneğin, kullanıcıdan bir metin girdisi almak için kullanılabilir.
* tkinter.filedialog: Kullanıcının dosya seçmesini sağlayan bir iletişim kutusu açar. Bu uygulamada, Excel dosyası kaydetmek için kullanılabilir.
* tkcalendar: Tkinter için takvim widget'ı sağlar. Yemek tarihlerini seçmek için kullanılabilir.
* sqlite3: Yerel bir SQLite veritabanına bağlanmak ve SQL sorguları çalıştırmak için kullanılır. Bu uygulamada, çalışan ve yemek bilgilerini saklamak için kullanılır.
* datetime: Tarih ve saatle ilgili işlemler yapmak için kullanılır. Yemek tarihlerini işlemek için kullanılır.
* os: İşletim sistemiyle etkileşim kurmak için kullanılan bir modüldür. Dosya yolları ve diğer işletim sistemi kaynaklarıyla çalışmak için kullanılır.
* sys: Python yorumlayıcısı ile ilgili bilgileri sağlar. Bu uygulamada, uygulama yolunu bulmak için kullanılabilir.
* pandas: Veri analiz ve manipülasyonu için güçlü bir kütüphanedir. Excel dosyalarını işlemek ve verileri analiz etmek için kullanılır.
* openpyxl: Excel dosyalarını okumak, yazmak ve düzenlemek için kullanılır. Yemek verilerini Excel formatında kaydetmek için kullanılır.
* PIL (Pillow): Görüntü işleme kütüphanesidir. Bu uygulamada, logo veya diğer görselleri eklemek için kullanılabilir.
* calendar: Takvimle ilgili işlemler yapmak için kullanılır. Örneğin, bir ayın kaç günü olduğunu bulmak için kullanılabilir.
#### Uygulamanın Genel Yapısı
* Kullanıcı Arayüzü (UI): Tkinter ve ttk kullanılarak oluşturulan bir pencerede, çalışan ekleme, silme, arama, yemek ekleme, güncelleme gibi işlemler için butonlar, giriş kutuları, tablolar gibi öğeler bulunur.
* Veritabanı: SQLite veritabanında çalışanlar ve yemekler ile ilgili bilgiler saklanır.
#### İşlevsellik:
* Çalışan İşlemleri: Çalışan ekleme, silme, güncelleme ve arama gibi işlemler.
* Yemek İşlemleri: Yemek ekleme, güncelleme ve listeleme işlemleri.
* Excel Raporlama: Yemek verilerini Excel formatında dışa aktarma.
* Veritabanı İşlemleri: SQLite veritabanı ile etkileşim (veri ekleme, güncelleme, sorgulama).
