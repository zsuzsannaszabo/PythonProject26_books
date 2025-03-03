import gradio as gr
import pandas as pd
import os
import books_db_actions as db
from init_config import config



def get_books(user_input):

    if user_input:

        query = f"""select b."name", b.number_of_sales, b.reviews from authors a
                    join books b on a.author_id = b.author_id
                    where a."name" = '{user_input}'
                    order by b.number_of_sales desc;"""
        response = db.get_data(query, database_config)
        df = pd.DataFrame(response)

        if df.empty:
            raise Exception("Author was not found....")
        return df


    else:
        print("You need to insert an author before pressing the button")
        raise Exception("You need to insert an author before pressing the button")

def add_book(name, sales, review, author):
    if name and sales and review and author:
        if not sales.isnumeric():
            raise Exception("Sales parameter must be a number")
        if not review.isnumeric():
            raise Exception("Review must be a positive number")

        # if not author.isnumeric():
        #     raise Exception("Author must be a string")

        author_name = db.get_data(f"""select author_id from public.authors a where "name" = '{author}' limit 1;""", database_config)
        if len(author_name) > 0:
            author_id = author_name[0] ['author_id']
            db.insert_row(f"""insert into books(\"name\", number_of_sales, reviews, author_id) values ('{name}', {int(sales)}, {int(review)}, {int(author_id)});""",database_config)

        else:
            raise Exception("Author was not found in database")
        print(author_name)
    else:
        raise Exception("All values are mandatory")




    if int(sales) <= 0:
        raise Exception("Sales must be a positive number")

def delete_book(name):
    if name:
        db.delete_row(name, database_config)

    else:
        raise Exception("Book name is mandatory for deletion")

def table_change(table,author_name):
    print(table)
    original_table = get_books(author_name)
    if not original_table.equals(table):
        diff = original_table.compare(table)
        diff.get("r")
    print(original_table)







def start_gui_app():
    with gr.Blocks() as app:

        with gr.Row():
            with gr.Column(scale=1):
                author_input = gr.Textbox(label="Write an author")
            with gr.Column(scale=1):
                get_books_button = gr.Button("Show Books")

        with gr.Row():
            response_table = gr.Dataframe(label="Results", interactive=True)
            response_table.change(fn=table_change, inputs=[response_table, author_input])
            get_books_button.click(fn=get_books, inputs=author_input, outputs=response_table)

        with gr.Row():
            with gr.Column(scale=1):
                new_book = gr.Textbox(label="New Book")
            with gr.Column(scale=1):
                number_of_sales = gr.Textbox(label="Sales")
            with gr.Column(scale=1):
                review = gr.Textbox(label="Review")
            with gr.Column(scale=1):
                author = gr.Textbox(label="Author Name")
        with gr.Row():
            add_book_btn = gr.Button("Add Book")
            add_book_btn.click(fn=add_book, inputs=[new_book, number_of_sales, review, author])

        with gr.Row():
            with gr.Column(scale=1):
                delete_book_input = gr.Textbox(label="Delete book")
                delete_book_btn = gr.Button("Delete")
                delete_book_btn.click(fn=delete_book, inputs=delete_book_input)

            with gr.Column(scale=2):
                pass




    app.launch(inbrowser=True, show_error=True)



if __name__ == '__main__':
    database_config = config.get("database_config")
    database_config['password'] = os.environ['book_project']
    start_gui_app()