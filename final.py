import streamlit as st
import json

class DataManager:
    def __init__(self, filename):
        self.filename = filename
        self.data = {}

    def load_data(self):
        try:
            with open(self.filename, "r") as file:
                self.data = json.load(file)
        except FileNotFoundError:
            self.data = {}

    def save_data(self):
        with open(self.filename, "w") as file:
            json.dump(self.data, file)

class AthleteManager(DataManager):
    def __init__(self, filename):
        super().__init__(filename)

    def add_athlete(self, id, name, age, sport, sponsor):
        self.data[id] = {"name": name, "age": age, "sport": sport, "contact_details": sponsor, "performances": [], "sponsorship": None}
        self.save_data()  # Save data after adding athlete

    def delete_athlete(self, id):
        if id in self.data:
            del self.data[id]
            self.save_data()  # Save data after deleting athlete
            st.success("Athlete deleted successfully!")
        else:
            st.error("Athlete not found!")

    def edit_athlete(self, id, name, age, sport, sponsor):
        if id in self.data:
            self.data[id]["name"] = name
            self.data[id]["age"] = age
            self.data[id]["sport"] = sport
            self.data[id]["contact_details"] = sponsor
            self.save_data()  # Save data after editing athlete
            st.success("Athlete details updated successfully!")
        else:
            st.error("Athlete not found!")

    def add_performance(self, id, year, performance):
        if id in self.data:
            self.data[id]["performances"].append({"year": year, "performance": performance})
            self.save_data()  # Save data after adding performance
            st.success("Performance added successfully!")
        else:
            st.error("Athlete not found!")

    def view_athletes(self):
        st.subheader("Athlete Details:")
        for id, details in self.data.items():
            st.write(f"Athlete ID: {id}, Name: {details['name']}, Age: {details['age']}, Sport: {details['sport']}, contact details: {details['contact_details']}")
    
    def view_performances(self, id):
     if id in self.data:
        athlete_name = self.data[id]['name']
        performances = self.data[id]["performances"]
        years = [int(performance["year"]) for performance in performances]  # Convert years to integers
        performance_values = [performance["performance"] for performance in performances]

        # Generate descriptive report
        report = f"Athlete: {athlete_name}\n"
        report += "Year  Performance\n"
        report += "----------------------\n"
        for year, performance in zip(years, performance_values):
            report += f"{year} " +"    "+ f"{performance}\n"
        # Display report and graph
        st.write("Descriptive Report:")
        st.write(report)
     else:
        print("Athlete not found!")


# Load initial data
athlete_manager = AthleteManager("athletes.json")
athlete_manager.load_data()

athletes = {
    "admin": "password1",
    "athlete2": "password2",
    # Add more athletes as needed
}

sponsors = {
    "sponsor": "password1",
    "sponsor2": "password2",
    # Add more sponsors as needed
}

def athlete_login():
    if 'athlete_logged_in' not in st.session_state:
        st.session_state['athlete_logged_in'] = False

    if not st.session_state['athlete_logged_in']:
        username = st.text_input("Enter your admin username: ")
        password = st.text_input("Enter your admin password: ", type="password")

        if st.button("Login"):
            if username in athletes and athletes[username] == password:
                st.success("Admin login successful!")
                st.session_state['athlete_logged_in'] = True
            else:
                st.error("Invalid username or password.")
    else:
        st.success("Athlete already logged in!")

def sponsor_login():
    if 'sponsor_logged_in' not in st.session_state:
        st.session_state['sponsor_logged_in'] = False

    if not st.session_state['sponsor_logged_in']:
        username = st.text_input("Enter your sponsor username: ")
        password = st.text_input("Enter your sponsor password: ", type="password")

        if st.button("Login"):
            if username in sponsors and sponsors[username] == password:
                st.success("Sponsor login successful!")
                st.session_state['sponsor_logged_in'] = True
            else:
                st.error("Invalid username or password.")
    else:
        st.success("Sponsor already logged in!")

# Main program
def main():
    st.title("Athlete Sponsorship Management System")
    textbox="Welcome to our Athlete Sponsorship Management platform! Our homepage is your central hub for all things related to athlete sponsorship."
    st.sidebar.subheader(textbox)
    menu_option = st.sidebar.selectbox("Login as", ["Admin", "Sponsor"])

    if menu_option == "Admin":
        athlete_login()
        if st.session_state['athlete_logged_in']:
            st.empty()
            athlete_menu(athlete_manager)
    elif menu_option == "Sponsor":
        sponsor_login()
        if st.session_state['sponsor_logged_in']:
            st.empty()
            sponsor_menu(Sponsor(athlete_manager))

def athlete_menu(athlete_manager):
    st.subheader("Athlete Menu")
    menu_option = st.selectbox("Select an option", ["Add Athlete", "Edit Athlete", "Delete Athlete", "Add Performance", "View Athletes", "View Performances"])

    if menu_option == "Add Athlete":
        st.subheader("Add Athlete")
        id = st.text_input("Enter athlete ID")
        name = st.text_input("Enter athlete name")
        age = st.text_input("Enter athlete age")
        sport = st.text_input("Enter athlete sport")
        sponsor = st.text_input("Enter athlete Contact details")
        if st.button("Add Athlete"):
            athlete_manager.add_athlete(id, name, age, sport, sponsor)

    elif menu_option == "Edit Athlete":
        st.subheader("Edit Athlete")
        id = st.text_input("Enter athlete ID to edit")
        name = st.text_input("Enter new name")
        age = st.text_input("Enter new age")
        sport = st.text_input("Enter new sport")
        sponsor = st.text_input("Enter new contact")
        if st.button("Edit Athlete"):
            athlete_manager.edit_athlete(id, name, age, sport, sponsor)

    elif menu_option == "Delete Athlete":
        st.subheader("Delete Athlete")
        id = st.text_input("Enter athlete ID to delete")
        if st.button("Delete Athlete"):
            athlete_manager.delete_athlete(id)

    elif menu_option == "Add Performance":
        st.subheader("Add Performance")
        id = st.text_input("Enter athlete ID to add performance")
        year = st.text_input("Enter year of performance")
        performance = st.text_input("Enter performance value")
        if st.button("Add Performance"):
            athlete_manager.add_performance(id, year, performance)

    elif menu_option == "View Athletes":
        athlete_manager.view_athletes()

    elif menu_option == "View Performances":
        athlete_id = st.text_input("Enter athlete ID to view performances")
        if st.button("View Performances"):
            athlete_manager.view_performances(athlete_id)

def sponsor_menu(sponsor):
    st.subheader("Explore a diverse pool of athletes from various sports and demographics to find the perfect brand ambassador for your objectives.")
    st.subheader("Sponsor Menu")
    menu_option = st.selectbox("Select an option", ["Provide Sponsorship", "View Sponsorship", "View Athletes", "View Performances"])

    if menu_option == "Provide Sponsorship":
        st.subheader("Provide Sponsorship")
        athlete_id = st.text_input("Enter athlete ID to provide sponsorship")
        date = st.text_input("Enter sponsorship date")
        amount = st.text_input("Enter sponsorship amount")
        period = st.text_input("Enter sponsorship period")
        company_name = st.text_input("Enter company name")
        contact_details = st.text_input("Enter contact details")
        if st.button("Provide Sponsorship"):
            sponsor.provide_sponsorship(athlete_id, date, amount, period, company_name, contact_details)

    elif menu_option == "View Sponsorship":
        st.subheader("View Sponsorship")
        athlete_id = st.text_input("Enter athlete ID to view sponsorship")
        sponsor.view_sponsorship(athlete_id)

    elif menu_option == "View Athletes":
        sponsor.view_athletes()

    elif menu_option == "View Performances":
        athlete_id = st.text_input("Enter athlete ID to view performances")
        if st.button("View Performances"):
            sponsor.view_performances(athlete_id)

class Sponsor:
    def __init__(self, athlete_manager):
        self.athlete_manager = athlete_manager

    def provide_sponsorship(self, athlete_id, date, amount, period, company_name, contact_details):
        athlete = self.athlete_manager.data.get(athlete_id)
        if athlete:
            athlete["sponsorship"] = {
                "date": date,
                "amount": amount,
                "period": period,
                "company_name": company_name,
                "contact_details": contact_details
            }
            self.athlete_manager.save_data()  # Save data after providing sponsorship
            st.success(f"Sponsorship details added for Athlete {athlete['name']}.")
        else:
            st.error("Athlete not found!")

    def view_sponsorship(self, athlete_id):
        athlete = self.athlete_manager.data.get(athlete_id)
        if athlete:
            sponsorship = athlete.get("sponsorship")
            if sponsorship:
                st.subheader("Sponsorship Details")
                for key, value in sponsorship.items():
                    st.write(f"{key}: {value}")
            else:
                st.info("No sponsorship details found.")
        else:
            st.error("Athlete not found!")

    def view_athletes(self):
        self.athlete_manager.view_athletes()

    def view_performances(self, athlete_id):
        self.athlete_manager.view_performances(self, athlete_id)

if __name__ == "__main__":
    main()
