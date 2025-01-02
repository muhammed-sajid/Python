import tkinter as tk
from tkinter import Tk,filedialog,messagebox
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from tkinter import ttk




class DataScienceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Science with Tkinter")
        self.root.geometry("700x500")

        self.data = None

        #Button Layout
        self.load_button = tk.Button(root, text="Load CSV", command=self.load_data)
        self.load_button.pack(pady=10)

        self.column_label = tk.Label(root, text="Select Column for statistics:")
        self.column_label.pack()

        self.columns_combo = ttk.Combobox(root, state="readonly")
        self.columns_combo.pack(pady=5)

        self.stats_button = tk.Button(root, text="Show Statistics", command=self.show_statistics)
        self.stats_button.pack(pady=10)

        self.visualize_button = tk.Button(root, text="Visualize Data", command=self.visualize_data)
        self.visualize_button.pack(pady=10)

    def load_data(self):
        """ Load CSV data into a  pandas DataFrame"""
        file_path= filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            try:
                self.data = pd.read_csv(file_path)
                messagebox.showinfo("Success","File loaded successfully!")

                # populate the combobox with numerical columns from the dataset
                numerical_columns = self.data.select_dtypes(include=["number"]).columns.tolist()
                self.columns_combo["values"] =numerical_columns

                if len(numerical_columns) == 0:
                     messagebox.showwarning("No Numeric Columns",
                                            "The Dataset does not contain any numerical columns!")
            except Exception as e:
                messagebox.showerror("Error",
                                     f"Failed to load file: \n{str(e)}")

    def show_statistics(self):
        """ Display statistics (mean,median,mode) for the selected columns"""
        selected_col = self.columns_combo.get()
        if not selected_col or self.data is None:
            messagebox.showwarning("Error","Please select a column or load a dataset")
            return
        column = self.data[selected_col]
        mean_val = column.mean()
        median_val = column.median()
        mode_val = column.mode().values[0]

        stats_message = f"Statistics {selected_col}\n\nMean: {mean_val}\nMedian: {median_val}\nMode: {mode_val}"
        messagebox.showinfo("Statistics",stats_message)

    def visualize_data(self):
        if self.data is None:
            messagebox.showwarning("Error","Please Load a dataset first")
            return

        # prompt visualization options
        visualization_type = tk.StringVar(value="Histogram")

        def visualize():
            selected_visualization = visualization_type.get()
            selected_col = self.columns_combo.get()
            if selected_visualization == "Histogram":
                self.create_histogram(selected_col)
            elif selected_visualization == "Scatter Plot":
                self.create_scatterplot(selected_col)
            elif selected_visualization == "Box Plot":
                self.create_boxplot(selected_col)
            vis_windows.destroy()

        vis_windows = tk.Toplevel(self.root)
        vis_windows.title("Select visualization")

        vis_label = tk.Label(vis_windows, text="Select Visualization Type")
        vis_label.pack(pady=10)

        radio_hist = tk.Radiobutton(vis_windows, text="Histogram", variable=visualization_type, value="Histogram")
        radio_hist.pack(anchor="w")
        radio_scatter = tk.Radiobutton(vis_windows, text="Scatter Plot", variable=visualization_type, value="Scatter Plot")
        radio_scatter.pack(anchor="w")
        radio_box = tk.Radiobutton(vis_windows, text="Box Plot", variable=visualization_type, value="Box Plot")
        radio_box.pack(anchor="w")

        vis_button = tk.Button(vis_windows, text="Visualize", command=visualize)
        vis_button.pack(pady=10)

    def create_histogram(self,column_name):
        """ Create a histogram for the selected column """

        if column_name not in self.data.columns:
            messagebox.showerror("Error", "Please select a valid column for visualization.")
            return
        plt.figure(figsize=(8,6))
        sns.histplot(self.data[column_name], kde=True, color="blue")
        plt.title(f"Histogram of {column_name}")
        plt.xlabel(column_name)
        plt.ylabel("Frequency")
        plt.show()

    def create_scatterplot(self, column_name):
        """Create a scatter plot for the selected column against another column."""
        if column_name not in self.data.columns or len(self.data.columns) < 2:
            messagebox.showerror("Error", "Please ensure your dataset has multiple columns.")
            return

        # Choosing the second numerical column for scatter plot
        other_column = [col for col in self.data.columns if
                        col != column_name and pd.api.types.is_numeric_dtype(self.data[col])]
        if not other_column:
            messagebox.showwarning("Error", "No other numerical columns available for scatter plot!")
            return
        other_column = other_column[0]  # Use the first numerical column

        plt.figure(figsize=(8, 6))
        sns.scatterplot(x=self.data[column_name], y=self.data[other_column])
        plt.title(f"Scatter Plot: {column_name} vs {other_column}")
        plt.xlabel(column_name)
        plt.ylabel(other_column)
        plt.show()
    def create_boxplot(self,column_name):
        """Create a box plot for the selected column."""
        if column_name not in self.data.columns:
            messagebox.showerror("Error","please select a valid column for visualization.")
            return
        plt.figure(figsize=(8,6))
        sns.boxplot(x=self.data[column_name], color="green")
        plt.title(f"Box Plot of {column_name}")
        plt.xlabel(column_name)
        plt.show()


if __name__ == "__main__":
    root = Tk()
    app = DataScienceApp(root)
    root.mainloop()

