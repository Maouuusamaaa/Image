# Static Routing MikroTik — content notes

## Skema alamat

| Perangkat/interface | Alamat | Jaringan / fungsi |
|---|---|---|
| R1 bridge1 (LAN 1) | 192.168.1.1/24 | 192.168.1.0/24 |
| R1 ether1 (transit) | 172.16.1.1/30 | 172.16.1.0/30 |
| R2 ether1 (transit) | 172.16.1.2/30 | 172.16.1.0/30 |
| R2 bridge1 (LAN 2) | 192.168.2.1/24 | 192.168.2.0/24 |

## Router 1

```routeros
/ip address
add address=192.168.1.1/24 interface=bridge1
add address=172.16.1.1/30 interface=ether1

/ip route
add dst-address=192.168.2.0/24 gateway=172.16.1.2
```

## Router 2

```routeros
/ip address
add address=192.168.2.1/24 interface=bridge1
add address=172.16.1.2/30 interface=ether1

/ip route
add dst-address=192.168.1.0/24 gateway=172.16.1.1
```

## Verifikasi

```routeros
/ip/route/print
/ping 192.168.2.1
```

Jalankan ping dari R1 ke alamat LAN R2 dan sebaliknya. Setelah itu uji antar-klien dari dua LAN. Pastikan alamat IP, subnet mask, gateway klien, route balik, dan firewall sesuai. Hasil ping router-ke-router saja belum membuktikan seluruh trafik antar-klien diizinkan.
