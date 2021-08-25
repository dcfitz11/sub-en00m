import ssl
import requests
import pyfiglet
import time
from colorama import *
init(autoreset=True)

# COLOR VARIABLES:
reset = Fore.RESET
red = Fore.RED
yellow = Fore.YELLOW
green = Fore.GREEN
magenta = Fore.MAGENTA


class Banner:
    ascii_banner = pyfiglet.figlet_format("SUBEN00M")
    print(yellow + ascii_banner)
    print("IG: " + magenta+ "@Cyb3r_dan")
    print("NOTE: results will be output to txt files in installation path.")


class Validate:
    def __init__(self, domain):
        self.domain = domain
        if not domain.endswith((".com", ".org", ".gov")):
            print(red + "\t" + domain + " is not a valid domain name")
            exit()
        else:
            pass


class SubEnoom:
    def __init__(self):
        self.grab_tgt()

    def grab_tgt(self):
        domain = input("\n{0}[+] Enter a domain to enumerate: ".format(yellow))
        Validate(domain)

        ans = input(yellow + "\n[+] Do you want to use your own wordlist against " + domain + "? [y/n]: ")
        if ans == "n".lower():
            print(yellow + "\n[+] Enumerating subdomains for " + domain + " on " + time.ctime())
            self.default(domain)
        elif ans == "y".lower():
            wordlist = input("Please specify a path to the wordlist")
            print(yellow + "\n[+] Enumerating subdomains for " + domain + " on " + time.ctime())
            self.usr_wordlist(domain, wordlist)
        else:
            self.grab_tgt()

    def default(self, domain):
        with open("subdomains.txt", "r") as f_obj:
            for subdomain in f_obj.readlines():
                subdomain = subdomain.strip("\n")
                self.enum(subdomain, domain)

    def usr_wordlist(self, domain, path):
        with open(path, "r") as f_obj:
            for subdomain in f_obj.readlines():
                subdomain = subdomain.strip("\n")
                self.enum(subdomain, domain)

    def enum(self, subdomain, domain):
        try:
            tgt = "https://" + subdomain + "." + domain
            r = requests.get(tgt, timeout=5)
            print("\t" + tgt + " " + green + "STATUS CODE <" + str(r.status_code) + ">")
            if r.status_code == 200:
                print(tgt, file=open("200.txt", "a"))
            elif r.status_code == 404:
                print(tgt, file=open("404.txt", "a"))
            elif r.status_code == 403:
                print(tgt, file=open("403.txt", "a"))
            else:
                print(tgt, file=open("other.txt", "a"))
        except KeyboardInterrupt:
            self.results()
        except(ssl.SSLCertVerificationError) as e:
            print("\t" + tgt + " STATUS CODE <NONE>")
            # print(red + "\t" + str(e))
        except(requests.exceptions.SSLError) as e:
            print("\t" + tgt + " STATUS CODE <NONE>")
            # print(red + "\t" + str(e))
        except(requests.exceptions.ConnectionError) as e:
            print("\t" + tgt + " STATUS CODE <NONE>")
            # print(red + "\t" + str(e))
        except(requests.exceptions.Timeout) as e:
            print("\t" + tgt + " STATUS CODE <NONE>")
            # print(red + "\t" + str(e))
        except(requests.TooManyRedirects) as e:
            print("\t" + tgt + " STATUS CODE <NONE>")
            # print(red + "\t" + str(e))

    def results(self):
        print(yellow + "\n------------------------------- RESULTS -------------------------------")
        print("Results were output to txt files for convenience.")
        print(yellow + "\n[+] 200 Status Codes: ")
        file_200 = open("200.txt", "r")
        for line in file_200:
            line = line.strip("\n")
            print(line)

        print(yellow + "\n[+] 404 Status Codes: ")
        file_404 = open("404.txt", "r")
        for line in file_404:
            line = line.strip("\n")
            print(line)

        print(yellow + "\n[+] 403 Status Codes: ")
        file_403 = open("other.txt", "r")
        for line in file_403:
            line = line.strip("\n")
            print(line)

        print(yellow + "\n[+] Other Status Codes: ")
        file_403 = open("other.txt", "r")
        for line in file_403:
            line = line.strip("\n")
            print(line)
        exit()



# START
Banner()
SubEnoom()


