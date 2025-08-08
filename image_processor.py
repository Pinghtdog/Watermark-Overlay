from PIL import Image

def add_overlay(base_image_path, overlay_image, output_path, position, scale, padding):
    """
    Pastes an overlay onto a base image and saves it.
    This function contains the core image manipulation logic.
    """
    try:
        base_image = Image.open(base_image_path).convert("RGBA")
        base_width, base_height = base_image.size

        # Resize overlay 
        new_overlay_width = int(base_width * scale)
        overlay_ratio = overlay_image.height / overlay_image.width
        new_overlay_height = int(new_overlay_width * overlay_ratio)
        resized_overlay = overlay_image.resize((new_overlay_width, new_overlay_height), Image.Resampling.LANCZOS)

        # Position overlay 
        padding_px = int(base_width * padding)
        if position == 'bottom-right':
            pos = (base_width - new_overlay_width - padding_px, base_height - new_overlay_height - padding_px)
        elif position == 'bottom-left':
            pos = (padding_px, base_height - new_overlay_height - padding_px)
        elif position == 'top-right':
            pos = (base_width - new_overlay_width - padding_px, padding_px)
        elif position == 'top-left':
            pos = (padding_px, padding_px)
        elif position == 'center':
            pos = (int((base_width - new_overlay_width)/2), int((base_height - new_overlay_height)/2))
        else:
            pos = (base_width - new_overlay_width - padding_px, base_height - new_overlay_height - padding_px)

        # Put overlay to base image
        transparent_layer = Image.new('RGBA', base_image.size, (0,0,0,0))
        transparent_layer.paste(resized_overlay, pos, resized_overlay)
        composited_image = Image.alpha_composite(base_image, transparent_layer)

      
        composited_image.save(output_path, "PNG")

        return True, None 
    except Exception as e:
        return False, str(e) 