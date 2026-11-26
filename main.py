# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import messagebox, simpledialog
import pygame
import os
from PIL import Image, ImageTk

from data_locations import LOCATIONS
from data_shop import SHOP_ITEMS


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Καστροπολιτεία")
        # Προσοχή: το προηγούμενο ήταν "1100x8500" (λάθος ύψος)
        self.root.geometry("1100x850")
        self.root.minsize(900, 700)

        # Κατάσταση εφαρμογής
        self.collection = []   # συλλογή πληροφοριών (τοποθεσίες)
        self.cart = []         # καλάθι αναμνηστικών

        # ΜΟΥΣΙΚΗ ΥΠΟΚΡΟΥΣΗ
        self.music_started = False
        self.init_music()

        # Εικόνα banner
        self.banner_img = None
        self.load_banner()

        # Κύριο frame περιεχομένου (single-page approach)
        self.frame = tk.Frame(root)
        self.frame.pack(fill="both", expand=True)

        # Αρχική οθόνη
        self.show_home()

    # ========== MULTIMEDIA ==========

    def init_music(self):
        """Αρχικοποίηση μουσικής υπόκρουσης με pygame."""
        try:
            pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=512)
            pygame.mixer.init()
            music_file = "music/theme.wav"

            if os.path.exists(music_file):
                pygame.mixer.music.load(music_file)
                pygame.mixer.music.set_volume(0.3)  # 0.1 = χαμηλά, 1.0 = δυνατά
                pygame.mixer.music.play(-1)         # -1 = επαναλαμβάνεται
                self.music_started = True
                print("Μουσική ξεκίνησε:", music_file)
            else:
                print("Αρχείο μουσικής δεν βρέθηκε:", music_file)
        except Exception as e:
            print("Σφάλμα μουσικής:", str(e))

    def load_banner(self):
        """Φόρτωση και προσαρμογή banner εικόνας."""
        try:
            img = Image.open("img/castle.jpg")
            img = img.resize((500, 250), Image.Resampling.LANCZOS)
            self.banner_img = ImageTk.PhotoImage(img)
            print("Banner φορτώθηκε!")
        except Exception as e:
            print("Banner σφάλμα:", e)

    def on_close(self):
        """Καθαρό κλείσιμο εφαρμογής και μουσικής."""
        try:
            pygame.mixer.music.stop()
            pygame.mixer.quit()
        except Exception:
            pass
        self.root.destroy()

    # ========== ΒΟΗΘΗΤΙΚΑ ==========

    def clear(self):
        """Καθαρίζει το περιεχόμενο του κεντρικού frame."""
        for w in self.frame.winfo_children():
            w.destroy()

    # ========== HOME / MENU ==========

    def show_home(self):
        """Αρχική οθόνη της εφαρμογής."""
        self.clear()

        if self.banner_img:
            img_label = tk.Label(self.frame, image=self.banner_img)
            img_label.image = self.banner_img  # reference για να μην κάνει garbage collect
            img_label.pack(pady=20)

        tk.Label(self.frame, text="Καστροπολιτεία",
                 font=("Arial", 22, "bold")).pack(pady=10)

        tk.Label(
            self.frame,
            text="Εξερεύνηση, μάθηση και αγορά αναμνηστικών σε μια εικονική καστροπολιτεία.",
            wraplength=800, justify="center"
        ).pack(pady=5)

        tk.Button(self.frame, text="Χάρτης", command=self.show_map,
                  width=20, height=2).pack(pady=5)
        tk.Button(self.frame, text="Κατάστημα Αναμνηστικών", command=self.show_shop,
                  width=20, height=2).pack(pady=5)
        tk.Button(self.frame, text="Συλλογή Γνώσεων", command=self.show_collection,
                  width=20, height=2).pack(pady=5)
        tk.Button(self.frame, text="Ξεναγήσεις", command=self.show_guides,
                  width=20, height=2).pack(pady=5)
        tk.Button(self.frame, text="Βοήθεια", command=self.show_help,
                  width=20, height=2).pack(pady=5)

    # ========== ΧΑΡΤΗΣ / ΤΟΠΟΘΕΣΙΕΣ ==========

    def show_map(self):
        """Εμφάνιση 'χάρτη' με όλες τις διαθέσιμες τοποθεσίες."""
        self.clear()
        tk.Label(self.frame, text="Σημεία Ενδιαφέροντος",
                 font=("Arial", 18, "bold")).pack(pady=10)

        tk.Label(
            self.frame,
            text="Επίλεξε μια περιοχή της καστροπολιτείας για να μάθεις περισσότερα.",
            wraplength=700
        ).pack(pady=5)

        for loc_id, loc in LOCATIONS.items():
            tk.Button(
                self.frame,
                text=loc["name"],
                command=lambda lid=loc_id: self.show_info(lid),
                width=30
            ).pack(pady=3)

        tk.Button(self.frame, text="Πίσω στην Αρχική", command=self.show_home).pack(pady=20)

    def show_info(self, loc_id):
        """Εμφάνιση λεπτομερειών για μια συγκεκριμένη τοποθεσία,
        μαζί με μικρές διαδραστικές δραστηριότητες.
        """
        self.clear()
        loc = LOCATIONS[loc_id]

        tk.Label(self.frame, text=loc["name"],
                 font=("Arial", 18, "bold")).pack(pady=10)
        tk.Label(self.frame, text=loc["description"],
                 wraplength=700, justify="left").pack(pady=5)

        tk.Label(self.frame, text=loc["info_title"],
                 font=("Arial", 14, "bold")).pack(pady=5)
        tk.Label(self.frame, text=loc["info_text"],
                 wraplength=700, justify="left").pack(pady=5)

        # Μικρές διαδραστικές δραστηριότητες ανάλογα με την τοποθεσία
        if loc_id == "ochiro":
            tk.Label(self.frame, text="Δραστηριότητα: Διάλεξε ρόλο φρουρού.",
                     font=("Arial", 12, "bold")).pack(pady=5)
            tk.Button(
                self.frame,
                text="Τοξότης",
                command=lambda: messagebox.showinfo(
                    "Τοξότης",
                    "Μαθαίνεις για τον εξοπλισμό του τοξότη και τον ρόλο του στην άμυνα."
                )
            ).pack(pady=2)
            tk.Button(
                self.frame,
                text="Λογχοφόρος",
                command=lambda: messagebox.showinfo(
                    "Λογχοφόρος",
                    "Βλέπεις πώς χρησιμοποιούσαν τις λόγχες και τις πανοπλίες τους."
                )
            ).pack(pady=2)

        if loc_id == "kouzina":
            tk.Label(self.frame, text="Δραστηριότητα: Επίλεξε εργαλείο μάγειρα.",
                     font=("Arial", 12, "bold")).pack(pady=5)
            tk.Button(
                self.frame,
                text="Χύτρα",
                command=lambda: messagebox.showinfo(
                    "Χύτρα",
                    "Η χύτρα χρησιμοποιούνταν για να μαγειρεύουν φαγητό για όλο το κάστρο."
                )
            ).pack(pady=2)
            tk.Button(
                self.frame,
                text="Μαχαίρι",
                command=lambda: messagebox.showinfo(
                    "Μαχαίρι",
                    "Με το μαχαίρι ετοίμαζαν τα υλικά για το μεσαιωνικό τραπέζι."
                )
            ).pack(pady=2)

        if loc_id == "kipos":
            tk.Label(self.frame, text="Δραστηριότητα: Διάλεξε ένα βότανο.",
                     font=("Arial", 12, "bold")).pack(pady=5)
            tk.Button(
                self.frame,
                text="Δεντρολίβανο",
                command=lambda: messagebox.showinfo(
                    "Δεντρολίβανο",
                    "Χρησιμοποιούνταν για να δίνει άρωμα στα φαγητά αλλά και σε γιατροσόφια."
                )
            ).pack(pady=2)
            tk.Button(
                self.frame,
                text="Χαμομήλι",
                command=lambda: messagebox.showinfo(
                    "Χαμομήλι",
                    "Το χαμομήλι λειτουργούσε ως ήπιο καταπραϋντικό και ρόφημα."
                )
            ).pack(pady=2)

        tk.Button(
            self.frame,
            text="Αποθήκευσε στη Συλλογή",
            command=lambda: self.save(loc)
        ).pack(pady=10)

        tk.Button(self.frame, text="Πίσω στον Χάρτη",
                  command=self.show_map).pack(pady=5)

    def save(self, loc):
        """Αποθήκευση τοποθεσίας στη συλλογή του χρήστη."""
        self.collection.append(loc)
        messagebox.showinfo("OK", "Η τοποθεσία αποθηκεύτηκε στη συλλογή σας!")

    def show_collection(self):
        """Εμφάνιση συλλογής αποθηκευμένων τοποθεσιών."""
        self.clear()
        tk.Label(self.frame, text="Συλλογή Γνώσεων",
                 font=("Arial", 18, "bold")).pack(pady=10)

        if not self.collection:
            tk.Label(self.frame, text="Δεν έχετε αποθηκεύσει ακόμα κάποια τοποθεσία.",
                     wraplength=700).pack(pady=10)
        else:
            for i, loc in enumerate(self.collection, 1):
                tk.Label(
                    self.frame,
                    text=f"{i}. {loc['name']} - {loc['description']}",
                    wraplength=700, justify="left"
                ).pack(pady=3)

        tk.Button(self.frame, text="Πίσω στην Αρχική", command=self.show_home).pack(pady=20)

    # ========== ΚΑΤΑΣΤΗΜΑ ΑΝΑΜΝΗΣΤΙΚΩΝ ==========

    def show_shop(self):
        """Οθόνη καταστήματος αναμνηστικών ειδών."""
        self.clear()
        tk.Label(self.frame, text="Κατάστημα Αναμνηστικών",
                 font=("Arial", 18, "bold")).pack(pady=10)

        tk.Label(
            self.frame,
            text="Επιλέξτε αναμνηστικά από την καστροπολιτεία και προσθέστε τα στο καλάθι σας.",
            wraplength=700
        ).pack(pady=5)

        for item in SHOP_ITEMS:
            frame_item = tk.Frame(self.frame)
            frame_item.pack(pady=3)

            tk.Label(
                frame_item,
                text=f"{item['name']} - €{item['price']}",
                width=60, anchor="w"
            ).pack(side="left")

            tk.Button(
                frame_item,
                text="Προσθήκη",
                command=lambda it=item: self.cart.append(it)
            ).pack(side="right")

        tk.Button(self.frame, text="Checkout (Εικονική Πληρωμή)",
                  command=self.checkout).pack(pady=15)
        tk.Button(self.frame, text="Πίσω στην Αρχική", command=self.show_home).pack(pady=5)

    def checkout(self):
        """Υλοποίηση checkout με χρήση 'εικονικής' πιστωτικής κάρτας."""
        if not self.cart:
            messagebox.showwarning("Καλάθι", "Το καλάθι σας είναι άδειο!")
            return

        total = sum(item["price"] for item in self.cart)

        # Εισαγωγή στοιχείων εικονικής κάρτας
        card_name = simpledialog.askstring(
            "Εικονική Κάρτα", "Όνομα κατόχου κάρτας:")
        if not card_name:
            return

        card_number = simpledialog.askstring(
            "Εικονική Κάρτα", "Αριθμός κάρτας (εικονικός, 16 ψηφία):")
        if not card_number:
            return

        messagebox.showinfo(
            "Πληρωμή",
            f"Συνολικό ποσό: €{total}\n"
            f"Κάρτα: {card_name}\n\n"
            "Η εικονική πληρωμή ολοκληρώθηκε με επιτυχία."
        )
        self.cart = []

    # ========== ΞΕΝΑΓΗΣΕΙΣ / ΑΦΗΓΗΣΕΙΣ ==========

    def show_guides(self):
        """Οθόνη με αφηγήσεις από ρόλους της καστροπολιτείας."""
        self.clear()
        tk.Label(self.frame, text="Ξεναγήσεις",
                 font=("Arial", 18, "bold")).pack(pady=10)

        tk.Label(
            self.frame,
            text="Επιλέξτε έναν ρόλο για να ακούσετε/διαβάσετε την αφήγησή του για τη ζωή στο κάστρο.",
            wraplength=700
        ).pack(pady=5)

        tk.Button(
            self.frame,
            text="Φρουρός",
            command=lambda: messagebox.showinfo(
                "Φρουρός",
                "Εγώ φυλάω τα τείχη μέρα-νύχτα, παρακολουθώντας τον ορίζοντα για κάθε κίνδυνο."
            )
        ).pack(pady=5)

        tk.Button(
            self.frame,
            text="Μάγειρας",
            command=lambda: messagebox.showinfo(
                "Μάγειρας",
                "Στην κουζίνα ετοιμάζω τα γεύματα για όλους, με όσα υλικά προσφέρει ο κήπος και η αγορά."
            )
        ).pack(pady=5)

        tk.Button(
            self.frame,
            text="Διοικητής",
            command=lambda: messagebox.showinfo(
                "Διοικητής",
                "Από τον πύργο μου παρακολουθώ την πόλη και παίρνω αποφάσεις για το καλό της καστροπολιτείας."
            )
        ).pack(pady=5)

        tk.Button(self.frame, text="Πίσω στην Αρχική", command=self.show_home).pack(pady=20)

    # ========== ON-LINE HELP ==========

    def show_help(self):
        """On-line βοήθεια χρήστη, όπως ζητείται από την εκφώνηση."""
        self.clear()
        tk.Label(self.frame, text="Βοήθεια Χρήσης",
                 font=("Arial", 18, "bold")).pack(pady=10)

        help_text = (
            "Καλώς ήρθατε στην εφαρμογή 'Καστροπολιτεία'!\n\n"
            "- Χάρτης: Εμφανίζει τις περιοχές του κάστρου. Κάνοντας κλικ σε μια περιοχή, "
            "βλέπετε ιστορικές πληροφορίες και μπορείτε να εκτελέσετε μικρές δραστηριότητες μάθησης.\n\n"
            "- Συλλογή Γνώσεων: Εδώ εμφανίζονται οι τοποθεσίες που έχετε αποθηκεύσει για μετέπειτα μελέτη.\n\n"
            "- Κατάστημα Αναμνηστικών: Σας επιτρέπει να προσθέσετε αναμνηστικά στο καλάθι και να ολοκληρώσετε "
            "εικονική πληρωμή με πιστωτική κάρτα.\n\n"
            "- Ξεναγήσεις: Παρέχει αφηγήσεις από ρόλους, όπως φρουρός, μάγειρας και διοικητής, "
            "που περιγράφουν τη ζωή στο κάστρο.\n\n"
            "Χρησιμοποιήστε τα κουμπιά 'Πίσω' για να επιστρέφετε στην προηγούμενη οθόνη."
        )

        tk.Label(self.frame, text=help_text,
                 wraplength=800, justify="left").pack(pady=10)

        tk.Button(self.frame, text="Πίσω στην Αρχική", command=self.show_home).pack(pady=20)


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()
