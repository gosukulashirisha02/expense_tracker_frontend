import streamlit as st
import requests
import pandas as pd

server_loc="http://127.0.0.1:8000"

st.title("Expensive Tracker Application")
opt=st.sidebar.selectbox("choose operations:--",["Add Expense","view Expense","Update Expense",
"Delete expense","Search expenses","Sort expenses","Filter expenses","analyse spending"])

if opt =="Add Expense":
    st.header("Adding Expense")
    with st.form("adding"):
        title=st.text_input("Expense Title")
        amount=st.number_input(
            "Amount",min_value=0.0
        )
        
        category=st.selectbox(
            "category",
            [
                "",
                "food",
                "travel",
                "shopping",
                "bills",
                "entertainment",
                "other"
            ]
        )
        
        btn=st.form_submit_button("Add Expense")
        
        if btn:
            
            new_data={
                "title":title,
                "amount":amount,
                "category":category
            }
            res=requests.post(f"{server_loc}/add_expense",
            json=new_data                  
            )
            st.write(res.json())
            

elif opt == "view Expense":

    if st.button("Get Expenses"):

        res = requests.get(
            f"{server_loc}/get_expenses"
        )

        all_expenses = res.json()

        df = pd.DataFrame(
            all_expenses["all_expenses"]
        )

        st.dataframe(df)
            
            
elif opt == "Update Expense":

    st.header("Update Expense")

    expense_id = st.number_input(
        "Expense ID",
        min_value=1,
        step=1
    )

    if st.button("Fetch Expense"):

        res = requests.get(
            f"{server_loc}/get_single_expense/{expense_id}"
        )

        if res.status_code == 200:

            expense_data = res.json()["expense_data"]

            st.session_state.title = expense_data["title"]
            st.session_state.amount = expense_data["amount"]
            st.session_state.category = expense_data["category"]

    title = st.text_input(
        "Title",
        value=st.session_state.get("title", "")
    )

    amount = st.number_input(
        "Amount",
        value=float(st.session_state.get("amount", 0))
    )

    category = st.text_input(
        "Category",
        value=st.session_state.get("category", "")
    )

    if st.button("Update Expense"):

        updated_data = {
            "title": title,
            "amount": amount,
            "category": category
        }

        res = requests.put(
            f"{server_loc}/update_expense/{expense_id}",
            json=updated_data
        )

        if res.status_code == 200:
            st.success(
                res.json()["updated_msg"]
            )


                        
elif opt =="Delete expense":
    st.header("Delete Expense")
    res=requests.get(f"{server_loc}/get_expenses")
    all_expenses=res.json()
    df=pd.DataFrame(
        all_expenses["all_expenses"]
    )
    st.dataframe(df)
    expense_id=st.number_input(
        "Expense ID To Delete",
        min_value=1
    )
    if st.button("Delete"):
        res=requests.delete(
            f"{server_loc}/delete_expense/{expense_id}"
        )
        if res.status_code==200:
            st.success(
                res.json()["msg_delete"]
            )
elif opt == "Search expenses":

    st.header("Search Expense")

    category = st.selectbox(
        "Choose Category",
        [
            "Food",
            "Travel",
            "Shopping",
            "Bills",
            "Entertainment",
            "Other"
        ]
    )

    if st.button("Search"):

        res = requests.get(
            f"{server_loc}/search_expense",
            params={
                "category": category
            }
        )

        if res.status_code == 200:

            data = res.json()

            df = pd.DataFrame(
                data["search_results"]
            )

            st.dataframe(df)
            
elif opt == "Sort expenses":

    st.header("Sort Expenses")

    sort_type = st.selectbox(
        "Sort By",
        [
            "date_desc",
            "date_asc",
            "price_desc",
            "price_asc"
        ]
    )

    if st.button("Sort"):

        res = requests.get(
            f"{server_loc}/sort_expenses",
            params={
                "sort_type": sort_type
            }
        )

        if res.status_code == 200:

            data = res.json()

            df = pd.DataFrame(
                data["sorted_expenses"]
            )

            st.dataframe(df)
            
elif opt == "Filter expenses":

    st.header("Filter Expenses")

    min_amount = st.number_input(
        "Minimum Amount",
        min_value=0.0,
        value=0.0
    )

    max_amount = st.number_input(
        "Maximum Amount",
        min_value=0.0,
        value=10000.0
    )

    if st.button("Filter"):

        res = requests.get(
            f"{server_loc}/filter_expenses",
            params={
                "min_amount": min_amount,
                "max_amount": max_amount
            }
        )

        if res.status_code == 200:

            data = res.json()

            df = pd.DataFrame(
                data["filtered_expenses"]
            )

            st.dataframe(df)

        else:
            st.error("Failed to fetch data")
     
       
elif opt == "analyse spending":

    st.header("Expense Analysis")

    if st.button("Analyze"):

        res = requests.get(
            f"{server_loc}/analyze_expenses"
        )

        if res.status_code == 200:

            data = res.json()

            st.subheader(
                f"Total Expense : ₹{data['total_expense']}"
            )

            st.subheader(
                "Category Wise Expense"
            )

            cat_df = pd.DataFrame(
                data["category_wise"]
            )

            st.dataframe(cat_df)

            st.bar_chart(
                cat_df.set_index("category")
            )
            
             
            
        
        
        
        
    