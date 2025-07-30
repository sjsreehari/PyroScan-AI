import datetime
import random



def unique_image_label(imagelabel):
    
    
    image_label = imagelabel.replace(".png", "")
    
    random_int = random.randint(99999999, 999999999999999)
    
    date_string_full = "30-07-25-21:49:56"
    format_string_full = "%d-%m-%y-%H:%M:%S"
    
    current_time = datetime.datetime.strptime(date_string_full, format_string_full)
    label = f"{image_label}-{random_int}-{current_time}".strip().replace(" ", "").replace(".", "").replace(":", "")

    label_name_with_ext = f"{label}.png"
    print(label_name_with_ext)
    
    return label_name_with_ext
