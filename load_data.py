import json
import sqlite3
from datetime import datetime
import os
import sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Import models from app.py
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app import app, db, Employee, Company, Job

def load_employee_data():
    """تحميل بيانات الموظفين من الملف JSON"""
    
    # قراءة بيانات الموظفين
    employees_data = [
        {
            "StaffNo": 10023099422738,
            "StaffName": "Salah Iqbal Fairfiri",
            "StaffName_ara": "صلاح اقبال فيرفيرى",
            "Job_Code": 1,
            "PassNo": "P9057652",
            "Nationality_Code": "IN",
            "Company_Code": "SQF",
            "CardNo": 100008759.0,
            "CardExpiryDate": 1755302400000,
            "CreateDateTime": 1735689600000
        },
        {
            "StaffNo": 10007099684673,
            "StaffName": "MUHAMED NIHAL PATTAMARU VALAPPIL",
            "StaffName_ara": "محمد نهال باتتمارو فالابيل",
            "Job_Code": 1,
            "PassNo": "P4167868",
            "Nationality_Code": "IN",
            "Company_Code": "UNI",
            "CardNo": 95697286.0,
            "CardExpiryDate": 1766188800000,
            "CreateDateTime": 1735689600000
        },
        {
            "StaffNo": 10005119743878,
            "StaffName": "MOHAMED FAYIZ ABOOBACKER",
            "StaffName_ara": "محمد فايز أبو بكر",
            "Job_Code": 1,
            "PassNo": "N8308013",
            "Nationality_Code": "IN",
            "Company_Code": "UNI",
            "CardNo": 102039520.0,
            "CardExpiryDate": 1752192000000,
            "CreateDateTime": 1735689600000
        },
        {
            "StaffNo": 50221069544283,
            "StaffName": "sami Ayshosh",
            "StaffName_ara": "سامى عیشوش",
            "Job_Code": 2,
            "PassNo": "17AA65462",
            "Nationality_Code": "IN",
            "Company_Code": "MNT",
            "CardNo": None,
            "CardExpiryDate": 1735689600000,
            "CreateDateTime": 1735689600000
        },
        {
            "StaffNo": 30219120007691,
            "StaffName": "Saleh Abdulaziz Heidari",
            "StaffName_ara": "صالح عبدالعزیز حیدري",
            "Job_Code": 2,
            "PassNo": None,
            "Nationality_Code": "IR",
            "Company_Code": "TAM",
            "CardNo": None,
            "CardExpiryDate": 1735689600000,
            "CreateDateTime": 1735689600000
        },
        {
            "StaffNo": 20010054470925,
            "StaffName": "Amina Othman Mohamed Othman",
            "StaffName_ara": "امینة عثمان محمد عثمان",
            "Job_Code": 2,
            "PassNo": "22222222",
            "Nationality_Code": "PK",
            "Company_Code": "TAM",
            "CardNo": None,
            "CardExpiryDate": 1735689600000,
            "CreateDateTime": 1735689600000
        },
        {
            "StaffNo": 30428119105516,
            "StaffName": "David John Sir Donsilo",
            "StaffName_ara": "ديفيد جون سير دونسيلو",
            "Job_Code": 2,
            "PassNo": "P7018817A",
            "Nationality_Code": "PH",
            "Company_Code": "SQF",
            "CardNo": 97660263.0,
            "CardExpiryDate": 1744848000000,
            "CreateDateTime": 1735689600000
        },
        {
            "StaffNo": 10024038496929,
            "StaffName": "SHEREEF SUBERKUTTY",
            "StaffName_ara": "شريف سوبركوتي سوبركوتي",
            "Job_Code": 2,
            "PassNo": "T6905780",
            "Nationality_Code": "IN",
            "Company_Code": "UNI",
            "CardNo": 92354549.0,
            "CardExpiryDate": 1759795200000,
            "CreateDateTime": 1735689600000
        },
        {
            "StaffNo": 10005057487546,
            "StaffName": "REVIKUMAR KOMPIPOYKAYIL THANKAN PAPPU THANKAN",
            "StaffName_ara": "ريفيكومار كومبيبوكايل تانكان بابو تانكان ريفيكومار كومبيبوكايل تانكان بابو تانكان",
            "Job_Code": 2,
            "PassNo": "R1129589",
            "Nationality_Code": "IN",
            "Company_Code": "UNI",
            "CardNo": 95736643.0,
            "CardExpiryDate": 1765670400000,
            "CreateDateTime": 1735689600000
        },
        {
            "StaffNo": 231078796633,
            "StaffName": "Ali Hassan Darweeish",
            "StaffName_ara": "على حسن درویش",
            "Job_Code": 2,
            "PassNo": None,
            "Nationality_Code": "LB",
            "Company_Code": "LIV",
            "CardNo": None,
            "CardExpiryDate": 1735689600000,
            "CreateDateTime": 1735689600000
        },
        {
            "StaffNo": 10013028094990,
            "StaffName": "SHAMEER PILATHOTTATHIL ALIKOYA ALIKOYA",
            "StaffName_ara": "شامير بيلاتوتاتيل عليكويا عليكويا",
            "Job_Code": 3,
            "PassNo": "N1900462",
            "Nationality_Code": "IN",
            "Company_Code": "UNI",
            "CardNo": 96044821.0,
            "CardExpiryDate": 1736726400000,
            "CreateDateTime": 1735689600000
        },
        {
            "StaffNo": 10029078505008,
            "StaffName": "Mohammed Akram Mohamad Aslam",
            "StaffName_ara": "محمد اكرم محمد اسلم",
            "Job_Code": 4,
            "PassNo": None,
            "Nationality_Code": "IN",
            "Company_Code": "LIV",
            "CardNo": None,
            "CardExpiryDate": 1735689600000,
            "CreateDateTime": 1735689600000
        },
        {
            "StaffNo": 31603127830586,
            "StaffName": "Rajindra Karki Bir Bahadur Karki",
            "StaffName_ara": "راجیندرا كاركى بیر بھادور كاركى",
            "Job_Code": 5,
            "PassNo": None,
            "Nationality_Code": "NB",
            "Company_Code": "MNT",
            "CardNo": None,
            "CardExpiryDate": 1735689600000,
            "CreateDateTime": 1735689600000
        },
        {
            "StaffNo": 20015097170910,
            "StaffName": "Nabeel Jameel Othman Jameel Othman",
            "StaffName_ara": "نبیل جمیل عثمان جمیل عثمان",
            "Job_Code": 5,
            "PassNo": None,
            "Nationality_Code": "PK",
            "Company_Code": "TAM",
            "CardNo": None,
            "CardExpiryDate": 1735689600000,
            "CreateDateTime": 1735689600000
        },
        {
            "StaffNo": 10031057039529,
            "StaffName": "Manoj Kumar Blathenam Madhavan Nair Thankaban Nair",
            "StaffName_ara": "مانوج كومار بلاتهانام مادهافان نایر تهانکابان نایر",
            "Job_Code": 5,
            "PassNo": "V1000612",
            "Nationality_Code": "IN",
            "Company_Code": "SQF",
            "CardNo": 95164228.0,
            "CardExpiryDate": 1740787200000,
            "CreateDateTime": 1735689600000
        },
        {
            "StaffNo": 10027078770191,
            "StaffName": "MUHAMMED MUSTHAFA VATTA PPARAMBIL POCKER VATTA PPARAMBIL",
            "StaffName_ara": "محمد مصطفى فاتّا برامبيل بوكر فاتّا برامبيل",
            "Job_Code": 5,
            "PassNo": "R4139111",
            "Nationality_Code": "IN",
            "Company_Code": "UNI",
            "CardNo": 100751647.0,
            "CardExpiryDate": 1752019200000,
            "CreateDateTime": 1735689600000
        },
        {
            "StaffNo": 10027119735334,
            "StaffName": "SHARUN KRISHNAN UNNIKRISHNAN CHANAYIL APPUKUTTAN",
            "StaffName_ara": "شارون كريشنان أونيكريشنان تشاناييل أبّوكوتّان",
            "Job_Code": 5,
            "PassNo": "U2390394",
            "Nationality_Code": "IN",
            "Company_Code": "UNI",
            "CardNo": 100664531.0,
            "CardExpiryDate": 1758153600000,
            "CreateDateTime": 1735689600000
        },
        {
            "StaffNo": 10030018069475,
            "StaffName": "ABDUL NASEER KARATT ANDUMAI HAJEE KARATT",
            "StaffName_ara": "عبد الناصر كارات أندوماي حاجي كارات",
            "Job_Code": 5,
            "PassNo": "V2112862",
            "Nationality_Code": "IN",
            "Company_Code": "UNI",
            "CardNo": 100878466.0,
            "CardExpiryDate": 1758931200000,
            "CreateDateTime": 1735689600000
        },
        {
            "StaffNo": 20004098385894,
            "StaffName": "Ambar Iqbal Jaweed Iqbal",
            "StaffName_ara": "عمبر اقبال جاوید اقبال",
            "Job_Code": 5,
            "PassNo": None,
            "Nationality_Code": "PK",
            "Company_Code": "LIV",
            "CardNo": None,
            "CardExpiryDate": 1735689600000,
            "CreateDateTime": 1735689600000
        },
        {
            "StaffNo": 30222097794745,
            "StaffName": "Saheela Ismail Bostan Shirin",
            "StaffName_ara": "سھیلا اسماعیل بستان شیرین",
            "Job_Code": 6,
            "PassNo": "H96889691",
            "Nationality_Code": "IR",
            "Company_Code": "BRG",
            "CardNo": None,
            "CardExpiryDate": 1735689600000,
            "CreateDateTime": 1735689600000
        },
        {
            "StaffNo": 50205056955247,
            "StaffName": "Oliver Biar Trombert",
            "StaffName_ara": "اولیفر بیار ترومبرت",
            "Job_Code": 6,
            "PassNo": "16FV15386",
            "Nationality_Code": "FR",
            "Company_Code": "TAM",
            "CardNo": None,
            "CardExpiryDate": 1735689600000,
            "CreateDateTime": 1735689600000
        },
        {
            "StaffNo": 10005098487148,
            "StaffName": "Irfan Riyaz Sorfi Sorfi Riyaz Mahmood",
            "StaffName_ara": "عرفان رياس سورفي سورفي ریاس محمود",
            "Job_Code": 6,
            "PassNo": "T0663585",
            "Nationality_Code": "PK",
            "Company_Code": "SQF",
            "CardNo": 95206068.0,
            "CardExpiryDate": 1746057600000,
            "CreateDateTime": 1735689600000
        },
        {
            "StaffNo": 10013028504393,
            "StaffName": "JAFILA VADAKKEYIL MOHAMED",
            "StaffName_ara": "جافيلة فاداكّيل محمد",
            "Job_Code": 6,
            "PassNo": "N8156535",
            "Nationality_Code": "IN",
            "Company_Code": "UNI",
            "CardNo": 95697210.0,
            "CardExpiryDate": 1766016000000,
            "CreateDateTime": 1735689600000
        },
        {
            "StaffNo": 10001075826745,
            "StaffName": "Syed Hussain Tahir Sayed Mohammad Tahir",
            "StaffName_ara": "سید حسین طاھر سید محمد طاھر",
            "Job_Code": 6,
            "PassNo": None,
            "Nationality_Code": "IN",
            "Company_Code": "LIV",
            "CardNo": None,
            "CardExpiryDate": 1735689600000,
            "CreateDateTime": 1735689600000
        },
        {
            "StaffNo": 20001099953341,
            "StaffName": "Majeed Ali Enayat Ali Otto",
            "StaffName_ara": "مجيد على عنايت على اوتو",
            "Job_Code": 7,
            "PassNo": "RZ1811152",
            "Nationality_Code": "PK",
            "Company_Code": "SQF",
            "CardNo": 101863410.0,
            "CardExpiryDate": 1763510400000,
            "CreateDateTime": 1735689600000
        },
        {
            "StaffNo": 10029069030602,
            "StaffName": "SAIRAJ RAJENDRAN NAIR SYAMALA THANKAPPAN PILLAI RAJENDRAN NAIR",
            "StaffName_ara": "سيراج راجيندران نایر سيامالا ثانكابان بيلاي راجيندران نایر",
            "Job_Code": 7,
            "PassNo": "V4436838",
            "Nationality_Code": "IN",
            "Company_Code": "UNI",
            "CardNo": 100663880.0,
            "CardExpiryDate": 1758153600000,
            "CreateDateTime": 1735689600000
        },
        {
            "StaffNo": 10010078495973,
            "StaffName": "MUHAMMED SABEER PULICKAL MOHAMMED KUTTY MOHAMMED KUTTY",
            "StaffName_ara": "محمد صبير بوليكل محمد كوتّي محمد كوتّي",
            "Job_Code": 7,
            "PassNo": "W7479240",
            "Nationality_Code": "IN",
            "Company_Code": "UNI",
            "CardNo": 102103581.0,
            "CardExpiryDate": 1754956800000,
            "CreateDateTime": 1735689600000
        },
        {
            "StaffNo": 10010087908201,
            "StaffName": "MOHAMED SAJEER ABDUL LATHIEF SALAHUDEEN",
            "StaffName_ara": "محمد ساجير عبد اللطيف صلاح الدين",
            "Job_Code": 8,
            "PassNo": "T9220979",
            "Nationality_Code": "IN",
            "Company_Code": "UNI",
            "CardNo": 97175724.0,
            "CardExpiryDate": 1766793600000,
            "CreateDateTime": 1735689600000
        },
        {
            "StaffNo": 10011069493421,
            "StaffName": "MOHAMMED SAFWAN UNNEENKUTTY",
            "StaffName_ara": "محمد صفوان أونينكوتّي",
            "Job_Code": 10,
            "PassNo": "N9611945",
            "Nationality_Code": "IN",
            "Company_Code": "UNI",
            "CardNo": 93325255.0,
            "CardExpiryDate": 1758412800000,
            "CreateDateTime": 1735689600000
        },
        {
            "StaffNo": 10001057739648,
            "StaffName": "SAKEER NOOH MOHAMMED NOOH",
            "StaffName_ara": "ساكير نوه محمد نوه",
            "Job_Code": 10,
            "PassNo": "N6229814",
            "Nationality_Code": "IN",
            "Company_Code": "UNI",
            "CardNo": 95828146.0,
            "CardExpiryDate": 1766448000000,
            "CreateDateTime": 1735689600000
        },
        {
            "StaffNo": 10029119051350,
            "StaffName": "YUNUS PUTHAN VEETTIL ASHARAF PUTHAN VEETTIL",
            "StaffName_ara": "يونس بُثان فيتّيل أشرف بُثان فيتّيل",
            "Job_Code": 10,
            "PassNo": "L8367568",
            "Nationality_Code": "IN",
            "Company_Code": "UNI",
            "CardNo": 95736623.0,
            "CardExpiryDate": 1737849600000,
            "CreateDateTime": 1735689600000
        },
        {
            "StaffNo": 10001069025786,
            "StaffName": "SAJEER MANGALASSER I PARAMBAT SHAREE MANGALASSER PARAMBATH",
            "StaffName_ara": "ساجير مانغالاسيري بارامباث شريف مانغالاسيري بارامباث",
            "Job_Code": 10,
            "PassNo": "R0363652",
            "Nationality_Code": "IN",
            "Company_Code": "UNI",
            "CardNo": 100178006.0,
            "CardExpiryDate": 1759881600000,
            "CreateDateTime": 1735689600000
        },
        {
            "StaffNo": 10003079469964,
            "StaffName": "YAWAR HUSAIN ANWAR HUSAIN",
            "StaffName_ara": "يوار حسين أنور حسين",
            "Job_Code": 10,
            "PassNo": "P4046288",
            "Nationality_Code": "IN",
            "Company_Code": "UNI",
            "CardNo": 100839432.0,
            "CardExpiryDate": 1765238400000,
            "CreateDateTime": 1735689600000
        },
        {
            "StaffNo": 10026038830628,
            "StaffName": "AJEESH RAVEENDRAN RAVEENDRA N VELAYUDAN",
            "StaffName_ara": "أجِيش رافيندران رافيندران فيلايودان",
            "Job_Code": 10,
            "PassNo": "V4944093",
            "Nationality_Code": "IN",
            "Company_Code": "UNI",
            "CardNo": 100663381.0,
            "CardExpiryDate": 1758412800000,
            "CreateDateTime": 1735689600000
        },
        {
            "StaffNo": 10002038512962,
            "StaffName": "ANEESH VISWANATH VISWANATHAN NAIR",
            "StaffName_ara": "أنيش فيسواناث فيسواناثان نایر",
            "Job_Code": 10,
            "PassNo": "S4679868",
            "Nationality_Code": "IN",
            "Company_Code": "UNI",
            "CardNo": 100828247.0,
            "CardExpiryDate": 1758844800000,
            "CreateDateTime": 1735689600000
        },
        {
            "StaffNo": 10013087071086,
            "StaffName": "MURALI BALARAMAN BALARAMAN",
            "StaffName_ara": "مورالي بالارامان بالارامان",
            "Job_Code": 10,
            "PassNo": "Z4040782",
            "Nationality_Code": "IN",
            "Company_Code": "UNI",
            "CardNo": 101020363.0,
            "CardExpiryDate": 1744243200000,
            "CreateDateTime": 1735689600000
        },
        {
            "StaffNo": 20027037653068,
            "StaffName": "Erum Iqbal Javid Iqbal",
            "StaffName_ara": "ایروم اقبال جاویداقبال",
            "Job_Code": 10,
            "PassNo": None,
            "Nationality_Code": "PK",
            "Company_Code": "LIV",
            "CardNo": None,
            "CardExpiryDate": 1735689600000,
            "CreateDateTime": 1735689600000
        },
        {
            "StaffNo": 20006079344248,
            "StaffName": "Syed Hussain Reza Abdi Syed Asad Reza Abdi",
            "StaffName_ara": "سید حسین رضا عابدى سید اسد رضا عابدى",
            "Job_Code": 11,
            "PassNo": None,
            "Nationality_Code": "PK",
            "Company_Code": "HON",
            "CardNo": None,
            "CardExpiryDate": 1735689600000,
            "CreateDateTime": 1735689600000
        },
        {
            "StaffNo": 20001016808218,
            "StaffName": "Yousuf Khan Hidayatullah Khan",
            "StaffName_ara": "یوسف خان ھدایت ﷲ خان",
            "Job_Code": 11,
            "PassNo": None,
            "Nationality_Code": "PK",
            "Company_Code": "HON",
            "CardNo": None,
            "CardExpiryDate": 1735689600000,
            "CreateDateTime": 1735689600000
        },
        {
            "StaffNo": 33021118419243,
            "StaffName": "Malikha Yaqoubdjanovna Othmanova",
            "StaffName_ara": "ملیكھ یاكوبدجانوفنا عثمانوفا",
            "Job_Code": 11,
            "PassNo": None,
            "Nationality_Code": "OZ",
            "Company_Code": "MNT",
            "CardNo": None,
            "CardExpiryDate": 1735689600000,
            "CreateDateTime": 1735689600000
        },
        {
            "StaffNo": 428108961308,
            "StaffName": "Yasmin Louay Danoura",
            "StaffName_ara": "یاسمین لؤى دنوره",
            "Job_Code": 11,
            "PassNo": None,
            "Nationality_Code": "SY",
            "Company_Code": "MNT",
            "CardNo": None,
            "CardExpiryDate": 1735689600000,
            "CreateDateTime": 1735689600000
        },
        {
            "StaffNo": 10026048658648,
            "StaffName": "KRISHNAKUMAR MADAMBAT H BALAKRISHNAN PAIKKATT",
            "StaffName_ara": "كريشناكومار مادامباث بالاكرشنان بايكات",
            "Job_Code": 11,
            "PassNo": "T5324324",
            "Nationality_Code": "IN",
            "Company_Code": "UNI",
            "CardNo": 102769335.0,
            "CardExpiryDate": 1746230400000,
            "CreateDateTime": 1735689600000
        },
        {
            "StaffNo": 10013079404478,
            "StaffName": "MUHAMMED RIFAD PULIYAN VEEDU",
            "StaffName_ara": "محمد رفاد بوليان فيدو",
            "Job_Code": 11,
            "PassNo": "L8839664",
            "Nationality_Code": "IN",
            "Company_Code": "UNI",
            "CardNo": 92354516.0,
            "CardExpiryDate": 1759795200000,
            "CreateDateTime": 1735689600000
        },
        {
            "StaffNo": 10016059320495,
            "StaffName": "KUNHUMOHAMMED MARAPARAMB ABDURAHIMAN MARAPARAMBIL",
            "StaffName_ara": "كونهمحمد مارابارامبيل عبد الرحيم مارابارامبيل",
            "Job_Code": 11,
            "PassNo": "K3052413",
            "Nationality_Code": "IN",
            "Company_Code": "UNI",
            "CardNo": 92617156.0,
            "CardExpiryDate": 1736294400000,
            "CreateDateTime": 1735689600000
        },
        {
            "StaffNo": 10028079561187,
            "StaffName": "AL ALIFKHAN BAVAKHAN",
            "StaffName_ara": "آل أليفخان بافاخان",
            "Job_Code": 11,
            "PassNo": "M5644020",
            "Nationality_Code": "IN",
            "Company_Code": "UNI",
            "CardNo": 93599220.0,
            "CardExpiryDate": 1760313600000,
            "CreateDateTime": 1735689600000
        },
        {
            "StaffNo": 10029018556649,
            "StaffName": "MOHAMMEDKHAN MUHAMMED ABDEEN MUHAMMED ABDEEN",
            "StaffName_ara": "محمدخان محمد عبدين محمد عبدين",
            "Job_Code": 11,
            "PassNo": "L2918664",
            "Nationality_Code": "IN",
            "Company_Code": "UNI",
            "CardNo": 94667421.0,
            "CardExpiryDate": 1766188800000,
            "CreateDateTime": 1735689600000
        },
        {
            "StaffNo": 10015079544680,
            "StaffName": "RAMSHAD ABDUL RASHEED ABDUL RASHEED KIZHAKKE KUTTY",
            "StaffName_ara": "رامشاد عبد الرشيد عبد الرشيد كيزهاكّي كوتّي",
            "Job_Code": 11,
            "PassNo": "M4981781",
            "Nationality_Code": "IN",
            "Company_Code": "UNI",
            "CardNo": 95886748.0,
            "CardExpiryDate": 1748822400000,
            "CreateDateTime": 1735689600000
        },
        {
            "StaffNo": 10019078090683,
            "StaffName": "ABDUL RAZZACK VALIYAKATH THARAYIL MAMMATH ABDULLA HAJI",
            "StaffName_ara": "عبد الرزاق فالياكات ثارايل مامات عبد الله حاجي",
            "Job_Code": 11,
            "PassNo": "V1011593",
            "Nationality_Code": "IN",
            "Company_Code": "UNI",
            "CardNo": 96064631.0,
            "CardExpiryDate": 1756771200000,
            "CreateDateTime": 1735689600000
        },
        {
            "StaffNo": 10017069330500,
            "StaffName": "JESSEEM MOOLAMCODE BASHEER BASHEER MOOLAMCODE EBRAHIM",
            "StaffName_ara": "جسيم مولامكود بشير بشير مولامكود إبراهيم",
            "Job_Code": 11,
            "PassNo": "V6424084",
            "Nationality_Code": "IN",
            "Company_Code": "UNI",
            "CardNo": 98208398.0,
            "CardExpiryDate": 1762300800000,
            "CreateDateTime": 1735689600000
        },
        {
            "StaffNo": 10031038559786,
            "StaffName": "MUNSHEER AYAMUNNY PUTHIYA VEETIL",
            "StaffName_ara": "منشير أياموني بوتّيا فيتّيل",
            "Job_Code": 11,
            "PassNo": "P3455487",
            "Nationality_Code": "IN",
            "Company_Code": "UNI",
            "CardNo": 103119446.0,
            "CardExpiryDate": 1735689600000,
            "CreateDateTime": 1735689600000
        },
        {
            "StaffNo": 10031058629070,
            "StaffName": "DIPEESH DIVYAPRAKAS THRIPPAKKA DHAMODA RAN THRIPPAKKA L DIVYAPRAKASH",
            "StaffName_ara": "ديبيش ديفيابراكاش تريبّاكال داموداران تريبّاكال ديفيابراكاش",
            "Job_Code": 12,
            "PassNo": "R8124094",
            "Nationality_Code": "IN",
            "Company_Code": "UNI",
            "CardNo": 91898083.0,
            "CardExpiryDate": 1763942400000,
            "CreateDateTime": 1735689600000
        },
        {
            "StaffNo": 20016039741191,
            "StaffName": "ZIA UR REHMAN FOULAD KHAN",
            "StaffName_ara": "ضياء الرحمن فولاد خان",
            "Job_Code": 12,
            "PassNo": "NT9152682",
            "Nationality_Code": "PK",
            "Company_Code": "UNI",
            "CardNo": 97999213.0,
            "CardExpiryDate": 1747440000000,
            "CreateDateTime": 1735689600000
        },
        {
            "StaffNo": 10018049525671,
            "StaffName": "SABIN MAMPATTA BABURAJ BABURAJ",
            "StaffName_ara": "سابين مامباتا بابوراج بابوراج",
            "Job_Code": 12,
            "PassNo": "R1844137",
            "Nationality_Code": "IN",
            "Company_Code": "UNI",
            "CardNo": 100176084.0,
            "CardExpiryDate": 1759881600000,
            "CreateDateTime": 1735689600000
        },
        {
            "StaffNo": 30320078459058,
            "StaffName": "MOHAMED NIMNAS IMAM",
            "StaffName_ara": "محمد نِمنَس إمام",
            "Job_Code": 12,
            "PassNo": "N9420240",
            "Nationality_Code": "SR",
            "Company_Code": "UNI",
            "CardNo": 100839024.0,
            "CardExpiryDate": 1758326400000,
            "CreateDateTime": 1735689600000
        },
        {
            "StaffNo": 10017058613205,
            "StaffName": "SHAJAN SASI RAVINDRAN SASI",
            "StaffName_ara": "شاجان ساسي رافيندران ساسي",
            "Job_Code": 12,
            "PassNo": "U0829668",
            "Nationality_Code": "IN",
            "Company_Code": "UNI",
            "CardNo": 101436195.0,
            "CardExpiryDate": 1762732800000,
            "CreateDateTime": 1735689600000
        },
        {
            "StaffNo": 20016079546306,
            "StaffName": "IMRAN KHAN AMJAD HUSSAIN",
            "StaffName_ara": "عمران خان أمجد حسين",
            "Job_Code": 12,
            "PassNo": "GD4134932",
            "Nationality_Code": "PK",
            "Company_Code": "UNI",
            "CardNo": 88921659.0,
            "CardExpiryDate": 1766707200000,
            "CreateDateTime": 1735689600000
        },
        {
            "StaffNo": 30211026852486,
            "StaffName": "Syed Hameed Reza Syed Abdul Azim Mir Hashemi",
            "StaffName_ara": "سید حمید رضا سید عبدالعظیم میر ھاشمي",
            "Job_Code": 13,
            "PassNo": None,
            "Nationality_Code": "IR",
            "Company_Code": "HON",
            "CardNo": None,
            "CardExpiryDate": 1735689600000,
            "CreateDateTime": 1735689600000
        },
        {
            "StaffNo": 20019076662570,
            "StaffName": "Omran Mohammed Ali Mohammed Ali Naseeruddin",
            "StaffName_ara": "عمران محمد على محمد على نصیر الدین",
            "Job_Code": 14,
            "PassNo": None,
            "Nationality_Code": "PK",
            "Company_Code": "HON",
            "CardNo": None,
            "CardExpiryDate": 1735689600000,
            "CreateDateTime": 1735689600000
        },
        {
            "StaffNo": 30214126075595,
            "StaffName": "Mohammed Hassan Mohammed Reza Attar",
            "StaffName_ara": "محمد حسن محمد رضا عطار",
            "Job_Code": 14,
            "PassNo": None,
            "Nationality_Code": "IR",
            "Company_Code": "HON",
            "CardNo": None,
            "CardExpiryDate": 1735689600000,
            "CreateDateTime": 1735689600000
        },
        {
            "StaffNo": 30221037944813,
            "StaffName": "Mohammed Hussein Abdulhussein Layqi",
            "StaffName_ara": "محمدحسین عبدالحسین لایقى",
            "Job_Code": 15,
            "PassNo": "K96717673",
            "Nationality_Code": "IR",
            "Company_Code": "BRG",
            "CardNo": None,
            "CardExpiryDate": 1735689600000,
            "CreateDateTime": 1735689600000
        },
        {
            "StaffNo": 10006068338318,
            "StaffName": "Keer Ankumar Matireddy Matireddy Shinja Reddy",
            "StaffName_ara": "كير انكومار ماتيريدي ماتيريدي شینجا ریدی",
            "Job_Code": 16,
            "PassNo": "S6667720",
            "Nationality_Code": "IN",
            "Company_Code": "SQF",
            "CardNo": 94933377.0,
            "CardExpiryDate": 1766880000000,
            "CreateDateTime": 1735689600000
        },
        {
            "StaffNo": 10001068218598,
            "StaffName": "Sheikh Fareed Mohammed Ansari Ansari",
            "StaffName_ara": "شيك فريد محمد انصاري انصاري",
            "Job_Code": 16,
            "PassNo": "T2197937",
            "Nationality_Code": "IN",
            "Company_Code": "SQF",
            "CardNo": 95164228.0,
            "CardExpiryDate": 1740787200000,
            "CreateDateTime": 1735689600000
        },
        {
            "StaffNo": 20001018137363,
            "StaffName": "Mohammed Riyaz Qurban Hussain",
            "StaffName_ara": "محمد رياض قربان حسین",
            "Job_Code": 16,
            "PassNo": "AJ9914484",
            "Nationality_Code": "PK",
            "Company_Code": "SQF",
            "CardNo": 97059686.0,
            "CardExpiryDate": 1742601600000,
            "CreateDateTime": 1735689600000
        },
        {
            "StaffNo": 20020128596624,
            "StaffName": "Allah Bakhsh Mohammed Sharif",
            "StaffName_ara": "الله بخش محمد شریف",
            "Job_Code": 16,
            "PassNo": "DP3349452",
            "Nationality_Code": "PK",
            "Company_Code": "SQF",
            "CardNo": 97059687.0,
            "CardExpiryDate": 1743120000000,
            "CreateDateTime": 1735689600000
        },
        {
            "StaffNo": 10014079509107,
            "StaffName": "Abdullah Sufyan Mohammed Shamsuddin",
            "StaffName_ara": "عبدالله سفيان محمد شمس الدين",
            "Job_Code": 16,
            "PassNo": "N4909305",
            "Nationality_Code": "IN",
            "Company_Code": "SQF",
            "CardNo": 101469428.0,
            "CardExpiryDate": 1736553600000,
            "CreateDateTime": 1735689600000
        },
        {
            "StaffNo": 10022098726649,
            "StaffName": "Deepak Kumar Lahori Ram",
            "StaffName_ara": "ديباك كومار لاهورى رام",
            "Job_Code": 16,
            "PassNo": "M2759056",
            "Nationality_Code": "IN",
            "Company_Code": "SQF",
            "CardNo": 101466456.0,
            "CardExpiryDate": 1736553600000,
            "CreateDateTime": 1735689600000
        },
        {
            "StaffNo": 10018068643256,
            "StaffName": "Mohammed Riyaz Abdulhakim Abdulhakim",
            "StaffName_ara": "محمد رياس عبدالحكيم عبدالحكيم",
            "Job_Code": 16,
            "PassNo": "Z2653453",
            "Nationality_Code": "IN",
            "Company_Code": "SQF",
            "CardNo": 101750472.0,
            "CardExpiryDate": 1760140800000,
            "CreateDateTime": 1735689600000
        },
        {
            "StaffNo": 10016129046246,
            "StaffName": "Sameer Ghosh Sheikh",
            "StaffName_ara": "سامير غوس شيخ",
            "Job_Code": 16,
            "PassNo": "W5311278",
            "Nationality_Code": "IN",
            "Company_Code": "SQF",
            "CardNo": 101863411.0,
            "CardExpiryDate": 1763510400000,
            "CreateDateTime": 1735689600000
        },
        {
            "StaffNo": 30423047419204,
            "StaffName": "Alan Alajo Bimentel",
            "StaffName_ara": "الان الاجاو بيمينتيل",
            "Job_Code": 16,
            "PassNo": "P7337982B",
            "Nationality_Code": "PH",
            "Company_Code": "SQF",
            "CardNo": 101863773.0,
            "CardExpiryDate": 1763510400000,
            "CreateDateTime": 1735689600000
        },
        {
            "StaffNo": 20023019872323,
            "StaffName": "Hassan Noor Khatan",
            "StaffName_ara": "حسن نور خاتان",
            "Job_Code": 16,
            "PassNo": "LN6808152",
            "Nationality_Code": "PK",
            "Company_Code": "SQF",
            "CardNo": 101863412.0,
            "CardExpiryDate": 1763510400000,
            "CreateDateTime": 1735689600000
        },
        {
            "StaffNo": 20001019969631,
            "StaffName": "Abdul Sattar Mohammed Ashraf",
            "StaffName_ara": "عبدالستار محمد اشرف",
            "Job_Code": 16,
            "PassNo": "BY5421501",
            "Nationality_Code": "PK",
            "Company_Code": "SQF",
            "CardNo": 101863425.0,
            "CardExpiryDate": 1763510400000,
            "CreateDateTime": 1735689600000
        },
        {
            "StaffNo": 30223087018565,
            "StaffName": "Mohammed Farooq Ahmed Namur",
            "StaffName_ara": "محمد فاروق احمد نامور",
            "Job_Code": 17,
            "PassNo": "A97015284",
            "Nationality_Code": "IR",
            "Company_Code": "SQF",
            "CardNo": 97296854.0,
            "CardExpiryDate": 1741046400000,
            "CreateDateTime": 1735689600000
        },
        {
            "StaffNo": 10016079876632,
            "StaffName": "Jasim Ahmed Jamal Mohammed Jamal Mohammed",
            "StaffName_ara": "جاسم احمد جمال محمد جمال محمد",
            "Job_Code": 18,
            "PassNo": "P8781545",
            "Nationality_Code": "IN",
            "Company_Code": "SQF",
            "CardNo": 100963721.0,
            "CardExpiryDate": 1739145600000,
            "CreateDateTime": 1735689600000
        },
        {
            "StaffNo": 30230129351160,
            "StaffName": "Nasser Azizullah Aqili",
            "StaffName_ara": "ناصر عزيز الله عقيلى",
            "Job_Code": 19,
            "PassNo": "I96903974",
            "Nationality_Code": "IR",
            "Company_Code": "SQF",
            "CardNo": 101600049.0,
            "CardExpiryDate": 1752192000000,
            "CreateDateTime": 1735689600000
        }
    ]
    
    # استخدام Flask context
    with app.app_context():
        # مسح البيانات الموجودة إذا كانت موجودة
        Employee.query.delete()
        
        # إدراج بيانات الموظفين
        for emp in employees_data:
            # تحويل timestamps إلى datetime
            card_expiry = None
            create_date = None
            
            if emp['CardExpiryDate']:
                card_expiry = datetime.fromtimestamp(emp['CardExpiryDate'] / 1000)
            if emp['CreateDateTime']:
                create_date = datetime.fromtimestamp(emp['CreateDateTime'] / 1000)
                
            employee = Employee(
                staff_no=emp['StaffNo'],
                staff_name=emp['StaffName'],
                staff_name_ara=emp['StaffName_ara'],
                job_code=emp['Job_Code'],
                pass_no=emp['PassNo'],
                nationality_code=emp['Nationality_Code'],
                company_code=emp['Company_Code'],
                card_no=emp['CardNo'],
                card_expiry_date=card_expiry,
                create_date_time=create_date
            )
            db.session.add(employee)
        
        db.session.commit()
        print(f"تم تحميل {len(employees_data)} موظف بنجاح!")

if __name__ == '__main__':
    load_employee_data()
