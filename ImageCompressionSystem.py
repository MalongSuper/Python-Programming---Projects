# Optimized Image Compression System
import numpy as np
import scipy.spatial.distance as dist
from PIL import Image, ImageTk, UnidentifiedImageError, ImageEnhance
import cv2
import random
import tkinter as tk
from tkinter import filedialog, messagebox
from ortools.linear_solver import pywraplp


class KMean:
    def __init__(self, max_iters=100, tolerance=1e-4):
        self.max_iters = max_iters  # Maximum number of iterations
        self.tolerance = tolerance  # Threshold for the centroid movement

    def apply_kmeans(self, data, n_colors):
        labels = ''
        # Apply K-Mean Clustering with Scipy
        h, w, c = data.shape  # Get the image shape, typically (height, width, 3)
        data_reshaped = data.reshape(-1, 3)  # Reshape to 2D Array (use -1 instead of (h * w))
        # Step 1 - 2: Initialize centroids randomly from the data points
        # For example, if K = 16, we have 16 centroids
        centroids = np.array(random.sample(list(data_reshaped), n_colors))
        # Begin the K-Means iteration
        for iteration in range(self.max_iters):
            # Step 3: Assign each pixel to the nearest centroid using scipy cdist (faster than np.linalg.norm)
            # Step 3a: With K centroids, calculate the distance of the every centroid
            # to every point in the image, then choose the minimum one and mark its point
            distances = dist.cdist(data_reshaped, centroids, metric='euclidean')
            # Step 3b: With this, all the points are assigned to a cluster
            labels = np.argmin(distances, axis=1)
            # Step 4: Recalculate centroids as the mean of the assigned pixels
            # That is, we mark the center of each cluster
            # These center centroids are the new centroids of the cluster
            new_centroids = np.array([data_reshaped[labels == i].mean(axis=0) for i in range(n_colors)])
            # Handle empty clusters by reinitializing them to random data points
            for i in range(n_colors):
                if np.isnan(new_centroids[i]).any():
                    new_centroids[i] = data_reshaped[random.randint(0, data_reshaped.shape[0] - 1)]
            # Check for convergence
            if np.linalg.norm(new_centroids - centroids) < self.tolerance:
                break
            centroids = new_centroids
        # Step 5: Assign the final color (centroid) to each pixel
        compressed_data = centroids[labels].reshape(h, w, c).astype(int)
        return compressed_data

    def optimize_k(self, image_size):
        # OR-Tools to find the optimal K based on image size (height and width)
        solver = pywraplp.Solver.CreateSolver('SCIP')
        if not solver:
            return self.size_based_k(image_size)  # Use size-based fallback if solver is unavailable
        # Decision variables for K (the number of colors)
        lower_bound_K, upper_bound_K = 16, 1024
        K = solver.IntVar(lower_bound_K, upper_bound_K, 'K')  # K will be between 16 and 1024
        # Extract height and width from the image_size tuple
        h, w = image_size
        total_pixels = h * w
        # Constraints: Based on the image size
        if h >= 8192 and w >= 8192:  # If the image is 8192x8192 or above
            # K is within [512, 1024]
            lower_bound_K, upper_bound_K = 512, 1024
            lower_bound_size, upper_bound_size = 8192, 16384
        elif h >= 4096 and w >= 4096:  # If the image is 4096x4096 or above
            # K is within [256, 512]
            lower_bound_K, upper_bound_K = 256, 512
            lower_bound_size, upper_bound_size = 4096, 8192
        elif h >= 2048 and w >= 2048:  # If the image is 2048x2048 or above
            # K is within [128, 256]
            lower_bound_K, upper_bound_K = 128, 256
            lower_bound_size, upper_bound_size = 2048, 4096
        elif h >= 1024 and w >= 1024:  # If the image is 1024x1024 or above
            # K is within [64, 128]
            lower_bound_K, upper_bound_K = 64, 128
            lower_bound_size, upper_bound_size = 1024, 2048
        elif h >= 512 and w >= 512:  # If the image is 512x512 or above
            # K is within [32, 64]
            lower_bound_K, upper_bound_K = 32, 64
            lower_bound_size, upper_bound_size = 512, 1024
        elif h >= 256 and w >= 256:  # If the image is 256x256 or above
            # K is within [16, 32]
            lower_bound_K, upper_bound_K = 16, 32
            lower_bound_size, upper_bound_size = 256, 512
        else:  # If it is lower, K is fixed at 16
            lower_bound_K, upper_bound_K = 16, 16
            lower_bound_size, upper_bound_size = 0, 256
        # Add constraints
        solver.Add(K >= lower_bound_K)  # Lower bound constraint for K
        solver.Add(K <= upper_bound_K)  # Upper bound constraint for K
        # Calculate the expected value of K of the image range (by pixels) - Middle pixels point
        mean = ((lower_bound_size * lower_bound_size)
                + (upper_bound_size * upper_bound_size) // 2)
        mean_K = (lower_bound_K + upper_bound_K) // 2
        # Constraint based on given image size closeness to mean pixels
        if total_pixels >= mean:
            # Encourage K to be closer to the upper bound
            solver.Add(K >= mean_K)
            # Find the mean of middle pixels and the upper bound pixels
            middle_mean = ((mean + (upper_bound_size * upper_bound_size)) // 2)
            middle_K = (mean_K + upper_bound_K) // 2
            if total_pixels >= middle_mean:  # K leans to the upper bound of the midpoint interval
                solver.Add(K >= middle_K)
                # Constraints based on given image size difference to the bounds
                dist_lower = total_pixels - middle_mean
                dist_upper = upper_bound_size - total_pixels
                if dist_lower < dist_upper:  # K is minimized to the lower bound
                    solver.Add(K <= upper_bound_K)
                    solver.Minimize(K)
                else:  # K is maximized to the upper bound
                    solver.Add(K >= middle_K)
                    solver.Maximize(K)
            else:  # K leans to the lower bound of the midpoint interval
                solver.Add(K <= middle_K)
                # Constraints based on given image size difference to the bounds
                dist_lower = total_pixels - mean
                dist_upper = middle_mean - total_pixels
                if dist_lower < dist_upper:  # K is minimized to the lower bound of the midpoint interval
                    solver.Add(K <= middle_K)
                    solver.Minimize(K)
                else:  # K is maximized to the upper bound of the midpoint interval
                    solver.Add(K >= mean_K)
                    solver.Maximize(K)
        else:  # total_pixels < mean
            # Encourage K to be closer to the lower bound
            solver.Add(K <= mean_K)
            # Find the mean of middle pixels and the lower bound pixels
            middle_mean = ((mean + (upper_bound_size * upper_bound_size)) // 2)
            middle_K = (mean_K + upper_bound_K) // 2
            if total_pixels >= middle_mean:  # K leans to the upper bound of the midpoint interval
                solver.Add(K >= middle_K)
                # Constraints based on given image size difference to the bounds
                dist_lower = total_pixels - middle_mean
                dist_upper = mean - total_pixels
                if dist_lower < dist_upper:  # K is minimized to the lower bound
                    solver.Add(K <= mean_K)
                    solver.Minimize(K)
                else:  # K is maximized to the upper bound
                    solver.Add(K >= middle_K)
                    solver.Maximize(K)
            else:  # K leans to the lower bound of the midpoint interval
                solver.Add(K <= middle_K)
                # Constraints based on given image size difference to the bounds
                dist_lower = total_pixels - lower_bound_size
                dist_upper = middle_mean - total_pixels
                if dist_lower < dist_upper:  # K is minimized to the lower bound
                    solver.Add(K <= middle_K)
                    solver.Minimize(K)
                else:  # K is maximized to the upper bound
                    solver.Add(K >= lower_bound_K)
                    solver.Maximize(K)
        # Solve optimization problem
        status = solver.Solve()
        if status == pywraplp.Solver.OPTIMAL:
            optimal_K = int(K.solution_value())
            print(f"Optimal K found: {optimal_K}")
            return optimal_K
        else:
            return self.size_based_k(image_size)

    @staticmethod
    def size_based_k(image_size):  # If the optimization fails
        # Default K based on image size (Here, we use 1024 at maximum)
        h, w = image_size
        if h >= 8192 and w >= 8192:
            return 1024
        elif h >= 4096 and w >= 4096:
            return 512
        elif h >= 2048 and w >= 2048:
            return 256
        elif h >= 1024 and w >= 1024:
            return 128
        elif h >= 512 and w >= 512:
            return 64
        elif h >= 256 and w >= 256:
            return 32
        else:
            return 16  # Default value


class ImageCompressorApp:
    def __init__(self, root):
        self.root = root  # Main window
        self.root.title("Image Compression")
        self.root.geometry("400x200")
        self.root.resizable(False, False)
        # These are variables for GUI components
        self.compression_window = None
        self.input_path = None
        self.original_image = None
        self.cropped_image = None
        self.img_tk = None
        self.image_label = None
        self.size_label = None
        self.input_label = None
        self.k_select_menu = None
        self.window_label = None
        self.select_button = None
        self.format_var = None
        self.photo = None
        # Variables to store coordinates and rectangle
        self.start_x = None
        self.start_y = None
        self.rect = None
        # Scale components
        self.res_scale = None
        self.bright_scale = None
        self.color_scale = None
        self.blurry_scale = None
        self.adjusted_image = None
        # GUI Components
        self.create_widgets()

    def create_widgets(self):  # Add the elements to the screen
        # Label that will appear on the screen
        self.input_label = tk.Label(self.root, text="Welcome to the Image Compression Tool")
        self.input_label.pack(padx=10, pady=20)
        # Button "Select Image" will appear on the screen
        self.select_button = tk.Button(self.root, text="Select image to compress", command=self.select_image)
        self.select_button.pack(padx=10, pady=20)

    def select_image(self):
        # Open the dialog box for the user to select image
        self.input_path = filedialog.askopenfilename(title="Select image",
                                                     filetypes=[("Image", "*.jpg *.jpeg *.png *.bmp")])
        if self.input_path:
            self.original_image = cv2.imread(self.input_path)  # Store the original image
            self.cropped_image = None
            self.open_compression_window()  # Open the compression window
        else:
            messagebox.showwarning("Warning", "No image selected")

    def open_compression_window(self):
        self.compression_window = tk.Toplevel(self.root)
        self.compression_window.title("Compression Options")
        self.compression_window.geometry("800x800")
        self.compression_window.resizable(False, False)

        preview_label = tk.Label(self.compression_window, text="Image Preview")
        preview_label.pack(pady=5)

        img = cv2.resize(self.original_image, (450, 300))
        self.img_tk = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)))

        # Initialize self.image_label to store the preview image in compression_window
        self.image_label = tk.Label(self.compression_window, image=self.img_tk)
        self.image_label.image = self.img_tk
        self.image_label.pack(pady=5)

        # Display the size of the original image under the image preview
        size_frame = tk.Frame(self.compression_window)
        size_frame.pack(pady=8)
        self.size_label = tk.Label(size_frame,
                                   text=f"Size: {self.original_image.shape[0]} x {self.original_image.shape[1]}")
        self.size_label.pack(pady=5)

        # Create an option menu for selecting the number of colors
        k_frame = tk.Frame(self.compression_window)
        k_frame.pack(pady=10, fill="x")  # Fill x-axis to ensure alignment works properly
        # Align the "Choose colors" with the "Choose format to compress" label
        tk.Label(k_frame, text="\t\t\tChoose the number of colors:\t\t", anchor="w", width=46).pack(side=tk.LEFT)
        k_values = ["Optimize", 1024, 512, 256, 128, 64, 32, 16]
        self.k_select_menu = tk.StringVar(self.compression_window)
        self.k_select_menu.set("Optimize")  # Initial value
        # Dropdown menu for selecting K values
        k_menu = tk.OptionMenu(k_frame, self.k_select_menu, *k_values)
        k_menu.pack(side=tk.LEFT, pady=5)

        # Create the image format option
        formats_frame = tk.Frame(self.compression_window)
        formats_frame.pack(pady=10, fill="x")  # Fill x-axis to ensure alignment works properly
        # Display format options beneath the image
        tk.Label(formats_frame, text="\t\t\tChoose format to compress:\t\t", anchor="w", width=46).pack(side=tk.LEFT)
        self.format_var = tk.StringVar(value="jpg")
        formats = [("JPG", "jpg"), ("JPEG", "jpeg"), ("PNG", "png"), ("BMP", "bmp"), ("TIFF", "tiff")]
        for text, value in formats:  # Add radio button for the formats
            tk.Radiobutton(formats_frame, text=text, variable=self.format_var,
                           value=value, selectcolor="#4C9F70", indicatoron=False, width=5).pack(side=tk.LEFT)

        # Scale for adjusting image quality
        quality_frame = tk.Frame(self.compression_window)
        quality_frame.pack(pady=10)
        # Resolution label and scale
        resolution_label = tk.Label(quality_frame, text="Resolution:", fg="white")
        resolution_label.grid(row=0, column=0, padx=5, pady=(8, 0))
        # Resolution scale
        self.res_scale = tk.Scale(quality_frame, from_=10, to=120, orient="horizontal", width=10, length=200,
                                  variable=tk.IntVar(value=60), fg="white", command=lambda _: self.adjust_image())
        self.res_scale.grid(row=0, column=1, padx=10, pady=(0, 8))
        # Brightness label and scale
        brightness_label = tk.Label(quality_frame, text="Brightness:", fg="white")
        brightness_label.grid(row=0, column=2, padx=6, pady=(8, 2))
        # Brightness scale
        self.bright_scale = tk.Scale(quality_frame, from_=10, to=120, orient="horizontal", width=10, length=200,
                                     variable=tk.IntVar(value=60), fg="white", command=lambda _: self.adjust_image())
        self.bright_scale.grid(row=0, column=3, padx=12, pady=(2, 8))
        # Color label and scale
        color_label = tk.Label(quality_frame, text="Color:", fg="white")
        color_label.grid(row=1, column=0, padx=6, pady=(8, 2))
        # Color scale
        self.color_scale = tk.Scale(quality_frame, from_=10, to=120, orient="horizontal", width=10, length=200,
                                    variable=tk.IntVar(value=60), fg="white", command=lambda _: self.adjust_image())
        self.color_scale.grid(row=1, column=1, padx=12, pady=(2, 8))
        # Blurry label and scale
        blurry_label = tk.Label(quality_frame, text="Blurriness:", fg="white")
        blurry_label.grid(row=1, column=2, padx=6, pady=(8, 2))
        # Blurry scale
        self.blurry_scale = tk.Scale(quality_frame, from_=10, to=120, orient="horizontal", width=10, length=200,
                                     variable=tk.IntVar(value=60), fg="white", command=lambda _: self.adjust_image())
        self.blurry_scale.grid(row=1, column=3, padx=12, pady=(2, 8))

        # Image adjusting buttons
        button_frame = tk.Frame(self.compression_window)
        button_frame.pack(pady=10)
        # This button allows user to resize the image
        resize_button = tk.Button(button_frame, text="Resize Image", command=self.resize_image)
        resize_button.pack(side=tk.LEFT, padx=5, pady=10)
        # This button allows user to crop the image
        crop_button = tk.Button(button_frame, text="Crop Image", command=self.crop_image)
        crop_button.pack(side=tk.RIGHT, padx=10, pady=10)
        # This button allows user to compress the image
        compress_button = tk.Button(self.compression_window, text="Compress Image", width=20,
                                    command=lambda: self.process_image())
        compress_button.pack(pady=10)

        # Add window label for "image too large" warning
        self.window_label = tk.Label(self.compression_window, text="", fg="red")
        self.window_label.pack(pady=20)  # Ensure this is packed at the bottom of the window
        # After opening the window, check if the image is large
        img_size = self.original_image.shape[0] * self.original_image.shape[1]  # Pixels
        if img_size > 5_000_000:  # If the number of pixels exceeds 5 million
            self.window_label.config(text="Warning: Large image, compression might take some time", fg="red")
        else:
            self.window_label.config(text="", fg="red")  # Clear the warning if the image size is fine

    def crop_image(self):
        if not self.input_path:
            messagebox.showwarning("Warning", "Please select an image first")
            return
        # Create a separate window for cropping
        crop_window = tk.Toplevel(self.root)
        crop_window.title("Crop Image")
        crop_window.geometry("450x400")
        crop_canvas = tk.Canvas(crop_window, width=500, height=300)
        crop_canvas.pack()

        # Get the image and display it in this window
        img = cv2.imread(self.input_path)
        img = cv2.resize(img, (450, 300))
        self.img_tk = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)))
        crop_canvas.create_image(0, 0, image=self.img_tk, anchor="nw")

        # Manipulating the mouse's movements for cropping
        def on_mouse_down(event):
            self.start_x, self.start_y = event.x, event.y
            self.crop_rect = crop_canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y,
                                                          outline="red")

        def on_mouse_drag(event):
            crop_canvas.coords(self.crop_rect, self.start_x, self.start_y, event.x, event.y)

        def on_mouse_release(event):
            x1, y1, x2, y2 = map(int, crop_canvas.coords(self.crop_rect))
            self.cropped_image = img[y1:y2, x1:x2]

        def save_crop():
            # If a crop exists, proceed to update the image
            if hasattr(self, 'cropped_image') and self.cropped_image is not None:
                self.original_image = self.cropped_image  # Update the main image with the cropped version
                crop_window.destroy()
                self.update_size_display()  # Update size label in compression window
                self.update_compression_preview()  # Update the compression window with the cropped image
            else:  # If it is None, simply close the crop window
                crop_window.destroy()

        # Handle cropping process with mouse
        crop_canvas.bind("<ButtonPress-1>", on_mouse_down)
        crop_canvas.bind("<B1-Motion>", on_mouse_drag)
        crop_canvas.bind("<ButtonRelease-1>", on_mouse_release)

        crop_label = tk.Label(crop_window, text="Drag a part of the image you want to crop")
        crop_label.pack(padx=5, pady=5)
        save_button = tk.Button(crop_window, text="Save Crop", command=save_crop)
        save_button.pack(padx=10, pady=10)

    def update_size_display(self):  # This function is used to update the size display
        # When cropping or resizing is performed
        if self.original_image is not None:
            self.size_label.config(text=f"Size: {self.original_image.shape[0]} x {self.original_image.shape[1]}")
            self.window_label.config(text="")  # Remove the "Large Error" message

    def update_compression_preview(self):
        # Use cropped image if it exists; otherwise, revert to the original
        if self.cropped_image is not None:
            img = self.cropped_image
        else:
            img = self.original_image

        if img is None:
            messagebox.showerror("Error", "No image available for preview.")
            return

        img = cv2.resize(img, (450, 300))
        self.img_tk = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)))
        self.image_label.configure(image=self.img_tk)
        self.image_label.image = self.img_tk  # Keep a reference to avoid garbage collection

    # Add a method to adjust the image based on the scale values
    def adjust_image(self):
        if self.original_image is None:
            return
        # Clone the original image for manipulation
        adjusted_image = self.original_image.copy()
        # Read scale values
        resolution = self.res_scale.get()
        brightness = self.bright_scale.get()
        color = self.color_scale.get()
        blurriness = self.blurry_scale.get()
        # Adjust resolution (resize image)
        h, w = self.original_image.shape[:2]
        adjusted_image = cv2.resize(adjusted_image, (w * resolution // 100, h * resolution // 100),
                                    interpolation=cv2.INTER_LANCZOS4)
        # Convert from BGR (OpenCV) to RGB (Pillow) for brightness and color adjustments
        pil_image = Image.fromarray(cv2.cvtColor(adjusted_image, cv2.COLOR_BGR2RGB))
        # Adjust brightness
        enhancer = ImageEnhance.Brightness(pil_image)
        pil_image = enhancer.enhance(brightness / 60)  # Adjust brightness based on scale
        # Adjust color
        enhancer = ImageEnhance.Color(pil_image)
        pil_image = enhancer.enhance(color / 60)  # Adjust color based on scale
        # Convert back to BGR (OpenCV) after Pillow adjustments
        adjusted_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

        # Apply blurriness in BGR format
        if blurriness > 10:
            kernel_size = int((blurriness - 10) / 10) * 2 + 1  # Ensure kernel size is odd
            adjusted_image = cv2.GaussianBlur(adjusted_image, (kernel_size, kernel_size), 0)

        # Store the adjusted image for later use
        self.adjusted_image = adjusted_image

        # Update the preview with the adjusted image
        adjusted_image = cv2.resize(adjusted_image, (450, 300))
        self.img_tk = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(adjusted_image, cv2.COLOR_BGR2RGB)))
        self.image_label.configure(image=self.img_tk)
        self.image_label.image = self.img_tk  # Keep reference to avoid garbage collection

    def preview_image(self):  # New window to preview image
        preview_window = tk.Toplevel(self.root)
        preview_window.title("Image Preview")

        if self.cropped_image is not None:
            img = self.cropped_image
        else:
            img = cv2.imread(self.input_path)

        img = cv2.resize(img, (450, 300))
        img_tk = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)))
        img_label = tk.Label(preview_window, image=img_tk)
        img_label.image = img_tk
        img_label.pack()

    def update_compressed_image(self):
        # Update original image with the cropped image for compression
        if self.cropped_image is not None:
            self.original_image = self.cropped_image
        else:
            messagebox.showwarning("Warning", "No crop selected.")
        self.preview_image()  # Refresh preview with cropped image

    def reset_to_original(self):
        # Reload original image data
        self.original_image = cv2.imread(self.input_path)
        self.preview_image()  # Refresh preview with the original image

    def resize_image(self):
        # Create a new window for resizing
        resize_window = tk.Toplevel(self.root)
        resize_window.title("Resize Image")
        resize_window.geometry("300x250")
        # Instructions for selecting the size to resize
        tk.Label(resize_window, text="Select a size to resize the image:").pack(pady=10)
        sizes = [("2046x2046", (2046, 2046)),
                 ("1024x1024", (1024, 1024)),
                 ("512x512", (512, 512)),
                 ("256x256", (256, 256))]
        for size_name, size in sizes:
            tk.Button(resize_window, text=size_name,
                      command=lambda s=size: self.perform_resize(s, resize_window)).pack(pady=5)

    def perform_resize(self, size, resize_window):  # The resize is performed here
        if self.original_image is None:
            messagebox.showwarning("Warning", "No image loaded to resize.")
            return
        self.original_image = cv2.resize(self.original_image, size, interpolation=cv2.INTER_LANCZOS4)
        messagebox.showinfo("Success", f"Image resized to {size[0]}x{size[1]} successfully")
        resize_window.destroy()
        self.update_size_display()  # Update size label in compression window
        self.update_compression_preview()  # Update preview with resized image

    def process_image(self):
        output_format = self.format_var.get()  # Get the user's format option
        filetypes = {"jpg": [("JPG", "*.jpg")], "jpeg": [("JPEG", "*.jpeg")],
                     "png": [("PNG", "*.png")], "bmp": [("BMP", "*.bmp")], "tiff": [("TIFF", "*.tiff")]}
        # Open the dialog box to save image after compression, the option is the format selected
        try:
            output_path = filedialog.asksaveasfilename(title="Save image after compression",
                                                       defaultextension=f".{output_format}",
                                                       filetypes=filetypes[output_format])
        except KeyError:
            messagebox.showwarning("Error", "Please select a format for compression")
            return
        if not output_path:
            messagebox.showwarning("Warning", "No selected location")
            return
        # Processing manipulation
        try:
            if self.original_image is None:
                raise ValueError("No image is loaded for processing.")
            # Show "Processing..." message
            self.window_label.config(text="Processing...", fg="light green")
            self.window_label.update()  # Update the GUI immediately
            # Set adjusted_image, fallback to original_image if the scale is not adjusted
            image_to_compress = self.adjusted_image \
                if hasattr(self, 'adjusted_image') and self.adjusted_image is not None else self.original_image
            # Check if the image is empty before processing
            if image_to_compress is None or image_to_compress.size == 0:
                raise ValueError("No valid image to process.")
            # Convert OpenCV image format to numpy array (if necessary) and get size
            data = cv2.cvtColor(image_to_compress, cv2.COLOR_BGR2RGB)
            # Get image size (width * height) for OR-Tools optimization
            h, w, _ = image_to_compress.shape
            image_size = (h, w)  # Pass height and width to the optimizer
            # Use OR-Tools to optimize K based on the image size
            kmeans = KMean()
            # Get the selected value from the dropdown menu
            # Dictionary to map selected values to the corresponding number of colors
            k_values = {"Optimize": lambda: kmeans.optimize_k(image_size),
                        "1024": 1024, "512": 512, "256": 256,
                        "128": 128, "64": 64, "32": 32, "16": 16, }
            # Get the selected value
            selected_k = self.k_select_menu.get()
            # Set n_colors based on the selection
            n_colors = k_values.get(selected_k, 16)  # Default to 16 if not found
            # If the selected value is "Optimize - OR Tools", use the lambda function to get the optimal K
            if selected_k == "Optimize":
                n_colors = k_values[selected_k]()
            # Apply K-Means Clustering with the optimized n_colors (K)
            compressed_data = kmeans.apply_kmeans(data, n_colors)
            # The compressed image is saved in the output path of user's option
            self.save_image(compressed_data, output_path)
            # Inform the success of compression
            self.window_label.config(text="Compression Successful!!", fg="green")
            self.window_label.update()
            messagebox.showinfo("Success", f"Image saved at: {output_path}")
            self.window_label.config(text="")  # Return to normal

        except Exception as e:
            self.window_label.config(text="Unexpected error occurred", fg="red")
            messagebox.showerror("Error", f"Unexpected error occurred: {str(e)}")

    @staticmethod
    def load_image(image_path):
        try:
            img = Image.open(image_path).convert("RGB")  # Open the image and convert it
            data = np.array(img)  # Convert it into numpy array
            return data, img.size
        except UnidentifiedImageError:  # Inform if the image type is invalid
            raise ValueError("Unsupported image type. Please select another image")

    @staticmethod
    def save_image(data, output_path):  # Convert the compressed image to PIL image
        img = Image.fromarray(data.astype('uint8'), 'RGB')
        img.save(output_path)


# Run the code
root = tk.Tk()
app = ImageCompressorApp(root)
root.mainloop()
