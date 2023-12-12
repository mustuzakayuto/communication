from data.create import create_data_base_chat
from data.create import create_data_base_face
from data.create import create_db
from data.create import create_data_base_faceaverage
from data.create import create_data_base_image
from data.control import setchat

def main():
    create_data_base_chat.main()
    create_data_base_face.main()
    create_data_base_faceaverage.main()
    create_data_base_image.main()
    create_db.main()
    setchat.create_room_all()
if __name__ == "__main__":
    main()