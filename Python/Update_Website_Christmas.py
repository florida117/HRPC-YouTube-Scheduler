import requests
import os
from log_in import secrets

# Sets the location of the home folder
home_dir = os.path.expanduser("~")

# WordPress API credentials and endpoint
wp_url = 'https://hrpc.org.uk/wp-json/wp/v2'
page_id = '8157'  # Replace with your page ID. For videos, 8157
username = secrets.get('website_user_name')
password = secrets.get('website_password')

with open(home_dir + '/git/HRPC-YouTube-Scheduler/Service_Details/christmas_service_id.txt', 'r') as file:
    # Read the contents of the file
    video_url_1 = 'https://www.youtube.com/watch?v=' + file.read()
    
with open(home_dir + '/git/HRPC-YouTube-Scheduler/Service_Details/evening_service_id.txt', 'r') as file:
    # Read the contents of the file
    video_url_2 = ''

# Format the video URLs as embedded links
page_content = """[vc_row type="full_width_content" full_screen_row_position="middle" bg_image="7083" bg_position="center bottom" bg_repeat="no-repeat" scene_position="center" text_color="light" text_align="left" top_padding="16%" bottom_padding="5%" enable_gradient="true" color_overlay="#007daa" color_overlay_2="#004f7c" gradient_direction="left_t_to_right_b" overlay_strength="0.8" shape_divider_position="bottom" shape_type=""][vc_column centered_text="true" column_padding="no-extra-padding" column_padding_position="all" background_color_opacity="1" background_hover_color_opacity="1" column_shadow="none" column_border_radius="none" width="1/1" tablet_text_alignment="default" phone_text_alignment="default" column_border_width="none" column_border_style="solid"][vc_row_inner column_margin="default" text_align="left"][vc_column_inner column_padding="padding-1-percent" column_padding_position="bottom" background_color_opacity="1" background_hover_color_opacity="1" column_shadow="none" column_border_radius="none" width="1/1" column_border_width="none" column_border_style="solid"][vc_column_text]
<h1>Videos</h1>
[/vc_column_text][/vc_column_inner][/vc_row_inner][/vc_column][/vc_row][vc_row type="in_container" full_screen_row_position="middle" scene_position="center" text_color="dark" text_align="left" overlay_strength="0.3" shape_divider_position="bottom"][vc_column column_padding="no-extra-padding" column_padding_position="all" background_color_opacity="1" background_hover_color_opacity="1" column_shadow="none" column_border_radius="none" width="1/1" tablet_text_alignment="default" phone_text_alignment="default" column_border_width="none" column_border_style="solid"][vc_column_text css=".vc_custom_1709805682004{margin-top: 20px !important;margin-right: 20px !important;margin-bottom: 20px !important;margin-left: 20px !important;}"]
<h5>If you're unable to join us in person, we invite you to join us for Sunday worship via our online services. We'd also love to keep in touch with you! If you are not yet registered on ChurchSuite please get in touch by emailing <a href="mailto:office@hrpc.org.uk">office@hrpc.org.uk</a></h5>
[/vc_column_text][vc_row_inner column_margin="default" text_align="left"][vc_column_inner column_padding="no-extra-padding" column_padding_position="all" background_color_opacity="1" background_hover_color_opacity="1" column_shadow="none" column_border_radius="none" width="1/2" column_border_width="none" column_border_style="solid"][vc_video link=""" + '"' + video_url_1 + '"' + """][/vc_column_inner][vc_column_inner column_padding="no-extra-padding" column_padding_position="all" background_color_opacity="1" background_hover_color_opacity="1" column_shadow="none" column_border_radius="none" width="1/2" column_border_width="none" column_border_style="solid"][vc_video link=""" + '"' + video_url_2 + '"' + """][/vc_column_inner][/vc_row_inner][divider line_type="Full Width Line" line_thickness="1" divider_color="default" custom_height="5"][vc_custom_heading text="Previous services" google_fonts="font_family:Montserrat%3Aregular%2C700|font_style:400%20regular%3A400%3Anormal"][vc_column_text]Services from previous weeks can be accessed on our YouTube channel[/vc_column_text][nectar_btn size="small" button_style="regular" button_color_2="Accent-Color" icon_family="none" url="https://www.youtube.com/user/hrpcbangor" text="HRPC YouTube Channel" margin_top="10" margin_right="40%" margin_left="40%"][/vc_column][/vc_row]"""

# The data payload for the update
data = {
    'content': page_content
}

# Making the request
response = requests.post(
    f'{wp_url}/pages/{page_id}',
    json=data,
    auth=(username, password)  # Basic Auth
)

# Check if the request was successful
if response.status_code == 200:
    print("Page updated successfully!")
else:
    print(f"Failed to update page: {response.status_code}")
    print(response.text)