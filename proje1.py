import heapq
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque
from typing import Dict, List, Tuple, Optional

class Istasyon:
    def __init__(self, idx: str, ad: str, hat: str):
        self.idx = idx
        self.ad = ad
        self.hat = hat
        self.komsular: List[Tuple['Istasyon', int]] = []

    def komsu_ekle(self, istasyon: 'Istasyon', sure: int):
        self.komsular.append((istasyon, sure))

class MetroAgi:
    def __init__(self):
        self.istasyonlar: Dict[str, Istasyon] = {}

    def istasyon_ekle(self, idx: str, ad: str, hat: str):
        if idx not in self.istasyonlar:
            istasyon = Istasyon(idx, ad, hat)
            self.istasyonlar[idx] = istasyon

    def baglanti_ekle(self, istasyon1_id: str, istasyon2_id: str, sure: int):
        if istasyon1_id in self.istasyonlar and istasyon2_id in self.istasyonlar:
            istasyon1 = self.istasyonlar[istasyon1_id]
            istasyon2 = self.istasyonlar[istasyon2_id]
            istasyon1.komsu_ekle(istasyon2, sure)
            istasyon2.komsu_ekle(istasyon1, sure)

    def en_az_aktarma_bul(self, baslangic_id: str, hedef_id: str) -> Optional[List[Istasyon]]:
        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar:
            return None

        baslangic = self.istasyonlar[baslangic_id]
        hedef = self.istasyonlar[hedef_id]

        kuyruk = deque([(baslangic, [baslangic])])
        ziyaret_edildi = set()

        while kuyruk:
            mevcut_istasyon, rota = kuyruk.popleft()

            if mevcut_istasyon == hedef:
                return rota

            ziyaret_edildi.add(mevcut_istasyon)

            for komsu, _ in mevcut_istasyon.komsular:
                if komsu not in ziyaret_edildi:
                    kuyruk.append((komsu, rota + [komsu]))

        return None

    def en_hizli_rota_bul(self, baslangic_id: str, hedef_id: str) -> Optional[Tuple[List[Istasyon], int]]:
        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar:
            return None

        baslangic = self.istasyonlar[baslangic_id]
        hedef = self.istasyonlar[hedef_id]

        pq = [(0, baslangic, [baslangic])]
        ziyaret_edildi = {}

        while pq:
            toplam_sure, mevcut_istasyon, rota = heapq.heappop(pq)

            if mevcut_istasyon == hedef:
                return rota, toplam_sure

            if mevcut_istasyon in ziyaret_edildi and ziyaret_edildi[mevcut_istasyon] <= toplam_sure:
                continue

            ziyaret_edildi[mevcut_istasyon] = toplam_sure

            for komsu, sure in mevcut_istasyon.komsular:
                heapq.heappush(pq, (toplam_sure + sure, komsu, rota + [komsu]))

        return None

metro = MetroAgi()

metro.istasyon_ekle("K1", "Kızılay", "Kırmızı Hat")
metro.istasyon_ekle("K2", "Ulus", "Kırmızı Hat")
metro.istasyon_ekle("K3", "Demetevler", "Kırmızı Hat")
metro.istasyon_ekle("K4", "OSB", "Kırmızı Hat")

metro.baglanti_ekle("K1", "K2", 4)
metro.baglanti_ekle("K2", "K3", 6)
metro.baglanti_ekle("K3", "K4", 8)

print("\n🚇 En Az Aktarmalı Rota Testi:")
rota = metro.en_az_aktarma_bul("K1", "K4")

if rota:
    print("🛤️ En Az Aktarmalı Rota:", " -> ".join(i.ad for i in rota))
else:
    print("❌ Rota bulunamadı!")

print("\n🚅 En Hızlı Rota Testi:")
sonuc = metro.en_hizli_rota_bul("K1", "K4")

if sonuc:
    rota, sure = sonuc
    print(f"🛤️ En Hızlı Rota ({sure} dakika):", " -> ".join(i.ad for i in rota))
else:
    print("❌ Rota bulunamadı!")

G = nx.Graph()
for istasyon in metro.istasyonlar.values():
    G.add_node(istasyon.ad)

for istasyon in metro.istasyonlar.values():
    for komsu, _ in istasyon.komsular:
        G.add_edge(istasyon.ad, komsu.ad)

plt.figure(figsize=(8, 6))
nx.draw(G, with_labels=True, node_color="lightblue", edge_color="gray", node_size=3000, font_size=10)
plt.show()

































