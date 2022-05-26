from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
import selenium
from threading import Thread
from multiprocessing import Process
import time, sys, os

BASE_URL = "https://www.spider3d.co.il/wp-admin/admin.php?page=mailpoet-subscribers"
link = 'https://www.spider3d.co.il/wp-admin/admin.php?page=mailpoet-subscribers#/page[1]/sort_by[created_at]/sort_order[desc]/group[unconfirmed]'


class Scraper:
	def __init__(self, window, driver_path_fname) -> None:
		self.window = window
		self.driver_path_fname = driver_path_fname
		self.statuses = ["Subscribed", "Unconfirmed", "Unsubscribed", "Inactive", "Bounced"]
		self.init_driver()
		
	def init_driver(self):
		with open(self.window.driver_path_fname, "r") as f:
			self.driver_path = f.read()
			if not self.driver_path.endswith(".exe"):
				self.driver_path = os.path.join(self.driver_path, "chromedriver.exe")
		self.window.ui.textBrowser.append("Starting the automation system...")
		time.sleep(2)
		self.window.ui.textBrowser.append(f"Accessing Chrome web driver in {self.driver_path}...")
		opt = Options()
		opt.headless = True
		
		try:
			self.driver = webdriver.Chrome(self.driver_path)
		except:
			self.window.ui.textBrowser.append("Unable to access chromedriver!")
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
		self.window.ui.textBrowser.append("<< SIGN-IN >>\nEnter username:")
		Thread(target=self.on_user_input, args=(self.init_cred, "uname", "uname")).start()
		
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
		btn = self.driver.find_element_by_css_selector('a[class="itsec-pwls-login-fallback__link"]')
		btn.click()
		uname_elm = self.driver.find_element_by_css_selector('input[id="user_login"]')
		uname_elm.send_keys(self.uname)
		pass_elem = self.driver.find_element_by_css_selector('input[id="user_pass"]')
		pass_elem.send_keys(self.pword)
		submit = self.driver.find_element_by_css_selector('input[id="wp-submit"]')
		submit.click()
		try:
			wt = WebDriverWait(self.driver, 10).until(
				EC.presence_of_element_located((By.CSS_SELECTOR, 'span[class="mailpoet-categories-title"]'))
			)
			self.window.ui.status.setText("Signed in successfully!")
			print("Signed in successfully!")
			self.window.ui.status.setText("Begining Tasks!")
			print("Signed in successfully!")
			self.start()
		except:
			self.window.ui.status.setText("Invalid login!")
			print("Invalid login!")
			self.window.ui.start_btn.setText("Restart")
			self.window.ui.start_btn.setEnabled(True)


	def status_st(self, arg=None):
		if arg == "stat_amt":
			self.status_amount = self.window.ui.user_input.text()
			self.window.ui.user_input.setText("")
			self.window.ui.textBrowser.append("What status do you want to change to?")
			Thread(target=self.on_user_input, args=(self.status_st, "status_kw", "stat_kwd")).start()
		else:
			self.stat_kw = self.window.ui.user_input.text()
			self.window.ui.user_input.setText("")
			if self.stat_kw not in self.statuses:
				self.window.ui.textBrowser.append("Status does not exist! Try 'Subscribed':")
				Thread(target=self.on_user_input, args=(self.status_st, "status_kw", "stat_kwd")).start()
				return
			self.window.ui.textBrowser.append("Beginning Task...")
			self.prog()

	def start(self):
		print(self.driver.current_url)
		self.driver.get(link)
		time.sleep(5)
		print("\n"+self.driver.current_url)

		self.total_pages = 78
		# driver.find_element_by_class_name("mailpoet-listing-total-pages").text
		print(f"Total pages: {self.total_pages}\n")

		self.pages_list = []
		for i in range(1, int(self.total_pages)):
			lnk = f'https://www.spider3d.co.il/wp-admin/admin.php?page=mailpoet-subscribers#/page[{i}]/sort_by[created_at]/sort_order[desc]/group[unconfirmed]'
			self.pages_list.append(lnk)

		self.window.ui.textBrowser.append("How many status do you want changed?")
		Thread(target=self.on_user_input, args=(self.status_st, "stat_amt", "stat_amt")).start()

	def prog(self):
		self.tic = time.time()
		self.done_counting = False
		for page in self.pages_list:
			print(f"[*] Working on page: {page}\n")
			self.driver.get(page)
			print(self.driver.current_url, "\n")
			try:
				element = WebDriverWait(self.driver, 20).until(
					EC.presence_of_element_located((By.CSS_SELECTOR, 'a[class="mailpoet-listing-title"]'))
				)
				print("\nSeen!\n")
			except:
				sys.exit()
			mail_title_cls = "mailpoet-listing-title"
			mail_lists = self.driver.find_elements_by_class_name(mail_title_cls)
			mail_lists_links = []

			for j in mail_lists:
				mail_lists_links.append(j.get_attribute("href"))

			print(mail_lists_links)

			time.sleep(5)
			# input(f"Confirm changing {len(pages_list)} statuses")
			self.count = 0
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
					elem = WebDriverWait(self.driver, 20).until(
						EC.presence_of_element_located((By.CSS_SELECTOR, link_sel))
					)
					print("Located!\n")
				except Exception as e:
					print(f"\n[{str(e).upper()}] Timeout!\n")
					sys.exit()
				edit_link = self.driver.find_element_by_css_selector(link_sel)
				print(f"\n[*] Clicking on {edit_link.text}\n")
				self.window.ui.status.setText(f"Changing {edit_link.text} {' '*10}tasks done: {self.count}")
				edit_link.click()
				# driver.get(edit_link)
				time.sleep(2)
				print(f"\n[*]Changing Status\n")
				sel = Select(self.driver.find_element_by_css_selector('select[id="field_status"]'))
				sel.select_by_visible_text(self.stat_kw)
				time.sleep(2)
				try:
					save = self.driver.find_element_by_css_selector('button[class="button mailpoet-button button-primary"]').click()
				except Exception as e:
					print(e, "save")
				print(f"[*] Status changed successfully!")
				self.window.ui.status.setText(f"One status changed successfully!{' '*12}tasks done: {self.count}")
				self.count += 1

			if self.done_counting:
				break

		self.driver.close()