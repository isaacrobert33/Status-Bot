from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import selenium
from threading import Thread
from multiprocessing import Process
import time, os
import json, sys

BASE_URL = "https://www.spider3d.co.il/wp-admin/admin.php?page=mailpoet-subscribers"
link = 'https://www.spider3d.co.il/wp-admin/admin.php?page=mailpoet-subscribers#/page[1]/sort_by[created_at]/sort_order[desc]/group[unconfirmed]'

class Scraper:
	def __init__(self, window, driver_path_fname) -> None:
		self.window = window
		self.driver_path_fname = driver_path_fname
		self.statuses = ["Subscribed", "Unconfirmed", "Unsubscribed", "Inactive", "Bounced"]
		self.cred_path = os.path.join(os.environ["APPDATA"], "credentials.json")
		self.init_driver()
		
	def init_driver(self):
		with open(self.window.driver_path_fname, "r") as f:
			self.driver_path = rf'{f.read()}'
			if not self.driver_path.endswith(".exe"):
				self.driver_path = os.path.join(self.driver_path, "msedgedriver.exe")
		self.window.ui.textBrowser.append("Starting the automation system...")
		time.sleep(2)
		self.window.ui.textBrowser.append(f"Accessing web driver in {self.driver_path}...")
		opt = Options()
		opt.headless = True
		
		try:
			# self.driver = webdriver.Chrome(self.driver_path)
			s = Service(rf'{self.driver_path}')
			if not os.path.exists(self.driver_path):
				raise("Error")
			dr = [webdriver.Edge, webdriver.Chrome, webdriver.Firefox]
			self.driver = None
			for i in dr:
				try:
					self.driver = i.__call__(service=s)
					break
				except Exception as e:
					print(e)
		except Exception as e:
			self.window.ui.textBrowser.append("Unable to access chromedriver!")
			self.window.ui.textBrowser.append(f"Error output: {e}")
			self.window.ui.textBrowser.append("Please make sure it's in the path specified!")
			self.window.ui.textBrowser.append("Enter the correct path:")
			Thread(target=self.on_user_input, args=(self.save_driver_path, "driver_path", "driver_path")).start()
			
		try:
			self.driver.get(link)
			self.console_chat()
		except selenium.common.exceptions.WebDriverException:
			print("[*] No internet Connection!")
			self.window.ui.textBrowser.append("[!] No internet Connection! Please check your network settings.")
			self.window.ui.start_btn.setText("Restart")
			self.window.ui.start_btn.setEnabled(True)
	
	def console_chat(self):
		self.window.ui.textBrowser.append("<< SIGN-IN >>")
		if not os.path.exists(self.cred_path):
			self.window.ui.textBrowser.append("Enter username:")
			Thread(target=self.on_user_input, args=(self.init_cred, "uname", "uname")).start()
		else:
			self.sign_in()
		
	def on_user_input(self, callback, event, arg=None):
		self.window.set_event(event)
		while True:
			if getattr(self.window, event):
				callback.__call__(arg)
				break
	def save_driver_path(self, dt=None):
		print("saving..")
		with open(os.path.join(os.getenv("APPDATA"), "driver_path.txt"), "w") as f:
			f.write(self.window.ui.user_input.text())
		self.window.ui.user_input.setText("")
		self.window.ui.textBrowser.append("File path modified!")
		self.init_driver()

	def init_cred(self, cred):
		print("cred:", cred)
		if cred == "uname":
			self.uname = self.window.ui.user_input.text()
			self.window.ui.user_input.setText("")
			self.window.ui.textBrowser.append("Enter password:")
			Thread(target=self.on_user_input, args=(self.init_cred, "pword", "pword")).start()
		else:
			self.pword = self.window.ui.user_input.text()
			self.window.ui.user_input.setText("")
			print(self.uname, self.pword)
			self.window.ui.status.setText(f"Signing in to {self.uname}")
			self.sign_in()

	def sign_in(self):
		cred_path = os.path.join(os.environ["APPDATA"], "credentials.json")
		if not os.path.exists(cred_path):
			btn = self.driver.find_element_by_css_selector('a[class="itsec-pwls-login-fallback__link"]')
			btn.click()
			uname_elm = self.driver.find_element_by_css_selector('input[id="user_login"]')
			uname_elm.send_keys(self.uname)
			pass_elem = self.driver.find_element_by_css_selector('input[id="user_pass"]')
			pass_elem.send_keys(self.pword)
			submit = self.driver.find_element_by_css_selector('input[id="wp-submit"]')
			submit.click()
			try:
				wt = WebDriverWait(self.driver, 30).until(
					EC.presence_of_element_located((By.CSS_SELECTOR, 'span[class="mailpoet-categories-title"]'))
				)
				self.window.ui.status.setText("Signed in successfully!")
				print("Signed in successfully!")
				self.window.ui.status.setText("Begining Tasks!")
				print("Signed in successfully!")
				self.start()

				with open(cred_path, "w") as f:
					json.dump({"username": self.uname, "password": self.pword}, f, indent=4)

			except Exception as e:
				self.window.ui.status.setText("Invalid login!")
				print("Invalid login!", e)
				self.window.ui.start_btn.setText("Restart")
				self.window.ui.start_btn.setEnabled(True)
		else:
			with open(cred_path, "r") as f:

				data = json.load(f)
				self.uname = data["username"]
				self.pword = data["password"]
				self.window.ui.status.setText(f"Signing in to: {self.uname}")

				btn = self.driver.find_element_by_css_selector('a[class="itsec-pwls-login-fallback__link"]')
				btn.click()
				uname_elm = self.driver.find_element_by_css_selector('input[id="user_login"]')
				uname_elm.send_keys(self.uname)
				pass_elem = self.driver.find_element_by_css_selector('input[id="user_pass"]')
				pass_elem.send_keys(self.pword)
				submit = self.driver.find_element_by_css_selector('input[id="wp-submit"]')
				submit.click()
			try:
				wt = WebDriverWait(self.driver, 30).until(
					EC.presence_of_element_located((By.CSS_SELECTOR, 'span[class="mailpoet-categories-title"]'))
				)
				self.window.ui.status.setText("Signed in successfully!")
				print("Signed in successfully!")
				self.start()
			except Exception as e:
				self.window.ui.status.setText("Unable to sign in")
				print("Unable to sign_in", e)
				self.window.ui.start_btn.setText("Restart")
				self.window.ui.start_btn.setEnabled(True)

	def status_st(self, arg=None):
		if arg == "stat_amt":
			self.status_amount = self.window.ui.user_input.text()
			self.window.ui.user_input.setText("")
			self.prog()
		else:
			self.window.ui.user_input.setText("")
			self.window.ui.textBrowser.append("Beginning Task...")
			self.prog()

	def start(self):
		print(self.driver.current_url)
		self.driver.get(link)
		print("\n"+self.driver.current_url)
		try:
			wt = WebDriverWait(self.driver, 20).until(
				EC.presence_of_element_located((By.CSS_SELECTOR, 'span[class="mailpoet-categories-title"]'))
				)
			print("Total seen")
		except Exception as e:
			print("Timeout:", e)
			sys.exit()
		
		self.window.ui.textBrowser.append("How many status do you want changed?")
		Thread(target=self.on_user_input, args=(self.status_st, "stat_amt", "stat_amt")).start()

	def prog(self):
		self.tic = time.time()
		self.count = 0
		self.page = f'https://www.spider3d.co.il/wp-admin/admin.php?page=mailpoet-subscribers#/page[1]/sort_by[created_at]/sort_order[desc]/group[unconfirmed]'
		self.stat_kw = "Subscribed"

		try:
			self.driver.get(self.page)
			for status in range(0, int(self.status_amount)):
				def loader(page):
					
					print(self.driver.current_url, "\n")
					try:
						element = WebDriverWait(self.driver, 30).until(
							EC.presence_of_element_located((By.CSS_SELECTOR, 'a[class="mailpoet-listing-title"]'))
						)
						print("\nSeen!\n")
					except:
						time.sleep(3)
						sys.exit()
					mail_title_cls = "mailpoet-listing-title"
					mail_lists = [link.get_attribute("href") for link in self.driver.find_elements_by_class_name(mail_title_cls)]
					return mail_lists

				try:
					mail_lists_links = loader(self.page)
				except:
					time.sleep(3)
					mail_lists_links = loader(self.page)

				# print(mail_lists_links)
				link_sel = f'a[href="#{mail_lists_links[0].split("#")[1]}"]'
				try:
					elem = WebDriverWait(self.driver, 30).until(
						EC.presence_of_element_located((By.CSS_SELECTOR, link_sel))
					)
					print("Located!\n")
				except Exception as e:
					print(f"\n[{str(e).upper()}] Timeout!\n")
					time.sleep(5)
				try:
					edit_link = self.driver.find_element_by_css_selector(link_sel)
				except:
					print("Done already!")
					break

				print(f"\n[*] Clicking on {edit_link.text}\n")
				self.window.ui.status.setText(f"Changing {edit_link.text} {' '*10}tasks done: {self.count}")
				try:
					edit_link.click()
				except selenium.common.exceptions.ElementClickInterceptedException:
					time.sleep(5)
					try:
						edit_link.click()
					except:
						self.driver.get(self.page)
						continue
				# driver.get(edit_link)
				time.sleep(2)
				print(f"\n[*]Changing Status\n")
				try:
					sel = Select(self.driver.find_element_by_css_selector('select[id="field_status"]'))
					sel.select_by_visible_text(self.stat_kw)
				except Exception as e:
					print(e, "In getting status option")
					self.driver.get(self.page)
					continue
				time.sleep(1)
				try:
					save = self.driver.find_element_by_css_selector('button[type="submit"]').click()
				except Exception as e:
					print(e, "save")
					# if "intercepted" in str(e):
					print("Checking the save btn for a 2nd time!\n")
					time.sleep(3)
					try:
						sel = Select(self.driver.find_element_by_css_selector('select[id="field_status"]'))
						sel.select_by_visible_text(self.stat_kw)
						self.driver.find_element_by_css_selector('button[type="submit"]').click()
					except Exception as e:
						self.driver.get(self.page)
						print(e, "In Changing Status")
						continue
				print(f"[*] Status changed successfully!")
				self.window.ui.status.setText(f"One status changed successfully!{' '*12}tasks done: {self.count}")
				self.count += 1

			self.window.ui.status.setText(f"Done changing {self.count} status!")
			self.window.ui.textBrowser.append(f"Done with task in {round(time.time()-self.tic, 3)} sec")
			self.window.ui.start_btn.setEnabled(True)
			self.driver.close()

		except Exception as e:
			print("[!] Exception", e)
			self.window.ui.status.setText(f"Unable to accomplish task!!")
			self.window.ui.textBrowser.append(f"Task initialization failed!")
			self.window.ui.start_btn.setEnabled(True)
			self.window.ui.start_btn.setText("Restart")
			self.driver.close()


"""
time.sleep(5)
			# input(f"Confirm changing {len(pages_list)} statuses")
			print(f"Changing {self.status_amount}")
			for each in mail_lists_links:
				try:
					if int(self.status_amount) == self.count:
						self.window.ui.status.setText(f"Done changing {self.count} status!")
						self.window.ui.textBrowser.append(f"Done with task in {round(time.time()-self.tic, 3)} sec")
						self.done_counting = True
						self.window.ui.start_btn.setEnabled(True)
						break
				except:
					pass
				
				link_sel = f'a[href="#{each.split("#")[1]}"]'
				try:
					elem = WebDriverWait(self.driver, 30).until(
						EC.presence_of_element_located((By.CSS_SELECTOR, link_sel))
					)
					print("Located!\n")
				except Exception as e:
					print(f"\n[{str(e).upper()}] Timeout!\n")
					time.sleep(5)
				try:
					edit_link = self.driver.find_element_by_css_selector(link_sel)
				except:
					print("Done already!")
					break

				print(f"\n[*] Clicking on {edit_link.text}\n")
				self.window.ui.status.setText(f"Changing {edit_link.text} {' '*10}tasks done: {self.count}")
				try:
					edit_link.click()
				except selenium.common.exceptions.ElementClickInterceptedException:
					time.sleep(5)
					try:
						edit_link.click()
					except:
						self.driver.get(page)
						continue
				# driver.get(edit_link)
				time.sleep(2)
				print(f"\n[*]Changing Status\n")
				try:
					sel = Select(self.driver.find_element_by_css_selector('select[id="field_status"]'))
					sel.select_by_visible_text(self.stat_kw)
				except Exception as e:
					print(e, "In getting status option")
					self.driver.get(page)
					continue
				time.sleep(2)
				try:
					save = self.driver.find_element_by_css_selector('button[type="submit"]').click()
				except Exception as e:
					print(e, "save")
					# if "intercepted" in str(e):
					print("Checking the save btn for a 2nd time!\n")
					time.sleep(3)
					try:
						sel = Select(self.driver.find_element_by_css_selector('select[id="field_status"]'))
						sel.select_by_visible_text(self.stat_kw)
						self.driver.find_element_by_css_selector('button[type="submit"]').click()
					except:
						self.driver.get(page)
						continue
				print(f"[*] Status changed successfully!")
				self.window.ui.status.setText(f"One status changed successfully!{' '*12}tasks done: {self.count}")
				self.count += 1
				"""