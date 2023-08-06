"""
This assumes the types are the same in the source/destination projects
"""

import argparse
import tator

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--host', type=str, default='https://www.tatorapp.com')
    parser.add_argument('--token', type=str, required=True)
    parser.add_argument('--src-project', type=int, required=True)
    parser.add_argument('--src-section-name', type=str, required=True)
    parser.add_argument('--dest-project', type=int, required=True)
    parser.add_argument('--dest-section-name', type=str, required=True)

    args = parser.parse_args()

    tator_api = tator.get_api(host=args.host, token=args.token)

    # Get the media types in the source project
    media_types = tator_api.get_media_type_list(project=args.src_project)

    src_multi_type = []
    src_video_type = []
    src_image_type = []
    for media_type in media_types:
        if media_type.dtype == "multi":
            src_multi_type.append(media_type.id)

        elif media_type.dtype == "video":
            src_video_type.append(media_type.id)

        elif media_type.dtype == "image":
            src_image_type.append(media_type.id)

    if len(src_multi_type) != 1:
        logger.error(f"Multi type IDs: {src_multi_type}")
        raise ValueError(f"Invalid amount of multi media types in project {args.src_project}!")
    src_multi_type = src_multi_type[0]

    if len(src_video_type) != 1:
        logger.error(f"Video type IDs: {src_video_type}")
        raise ValueError(f"Invalid amount of video media types in project {args.src_project}!")
    src_video_type = src_video_type[0]

    if len(src_image_type) != 1:
        logger.error(f"Image type IDs: {src_image_type}")
        raise ValueError(f"Invalid amount of image media types in project {args.src_project}!")
    src_image_type = src_image_type[0]

    # Get the GPS type in source project
    src_gps_type = []
    state_types = tator_api.get_state_type_list(project=args.src_project)
    for state_type in state_types:
        if state_type.name == "GPS":
            src_gps_type.append(state_type.id)

    if len(src_gps_type) != 1:
        logger.error(f"GPS type IDs: {src_gps_type}")
        raise ValueError(f"Invalid amount of GPS state types in project {args.src_project}!")
    src_gps_type = src_gps_type[0]

    # Get the corresponding section ID
    src_section = tator_api.get_section_list(
        project=args.src_project, name=args.src_section_name)[0].id

    if args.dest_project == args.src_project:
        dest_multi_type = src_multi_type
        dest_video_type = src_video_type
        dest_image_type = src_image_type
        dest_gps_type = src_gps_type

    else:
        media_types = tator_api.get_media_type_list(project=args.src_project)

        dest_multi_type = []
        dest_video_type = []
        dest_image_type = []
        for media_type in media_types:
            if media_type.dtype == "multi":
                dest_multi_type.append(media_type.id)

            elif media_type.dtype == "video":
                dest_video_type.append(media_type.id)

            elif media_type.dtype == "image":
                dest_image_type.append(media_type.id)

        if len(dest_multi_type) != 1:
            logger.error(f"Multi type IDs: {dest_multi_type}")
            raise ValueError(f"Invalid amount of multi media types in project {args.dest_project}!")
        dest_multi_type = dest_multi_type[0]

        if len(dest_video_type) != 1:
            logger.error(f"Video type IDs: {dest_video_type}")
            raise ValueError(f"Invalid amount of video media types in project {args.dest_project}!")
        dest_video_type = dest_video_type[0]

        if len(src_image_type) != 1:
            logger.error(f"Image type IDs: {dest_image_type}")
            raise ValueError(f"Invalid amount of image media types in project {args.dest_project}!")
        dest_image_type = src_image_type[0]

        # Get the GPS type in source project
        dest_gps_type = []
        state_types = tator_api.get_state_type_list(project=args.dest_project)
        for state_type in state_types:
            if state_type.name == "GPS":
                dest_gps_type.append(state_type.id)

        if len(dest_gps_type) != 1:
            logger.error(f"GPS type IDs: {dest_gps_type}")
            raise ValueError(f"Invalid amount of GPS state types in project {args.dest_project}!")
        dest_gps_type = dest_gps_type[0]

    # Create the new trip/section in the target project
    #response = tator_api.create_section_list(project=dest_project, name=args.dest_section_name)
    #dest_section = tator_api.get_section_list(id=response.id)

    # Create the new single-view trip/section in the target project
    #response = tator_api.create_section_list(project=dest_project, name=args.dest_single_view_section)
    #dest_single_view_section = tator_api.get_section_list(id=response.id)

    # Grab the multviews we care about
    src_multis = tator_api.get_media_list(
        project=args.src_project, type=src_multi_type, section=src_section)

    # Clone the new multi-view media
    media_ids = []
    for multi in src_multis:
        media_ids.append(multi.id)

    spec = {
      "dest_project": args.dest_project,
      "dest_type": dest_multi_type,
      "dest_section": args.dest_section_name
    }
    response = tator_api.clone_media_list(
        project=args.src_project, media_id=media_ids, clone_media_spec=spec)
    print(response)

    multi_id_mapping = {} # Keys = src multi ID, value = corresponding dest multi ID
    for src_multi_id, dest_multi_id in zip(media_ids, response.id):
        multi_id_mapping[src_multi_id] = dest_multi_id

    dest_section = tator_api.get_section_list(project=args.dest_project, name=args.dest_section_name)[0]
    dest_section_tator_user_sections = dest_section.tator_user_sections
    dest_section = dest_section.id
    dest_multis = tator_api.get_media_list(
        project=args.dest_project, type=dest_multi_type, section=dest_section)

    # Clone the single videos and update the new multi-view media
    prime_video_mapping = {} # Keys = src_multi.media_files.ids[0], values = dest_multi.media_files.ids
    for src_multi in src_multis:

        dest_multi_id = multi_id_mapping[src_multi.id]
        dest_multi = tator_api.get_media(dest_multi_id)

        spec = {
          "dest_project": args.dest_project,
          "dest_type": dest_video_type,
          "dest_section": args.dest_section_name + " singleview"
        }
        response = tator_api.clone_media_list(
            project=args.dest_project, media_id=src_multi.media_files.ids, clone_media_spec=spec)
        print(response)

        dest_videos = response.id
        dest_multi.media_files.ids = dest_videos
        media_update_spec = {"media_files": dest_multi.media_files}
        response = tator_api.update_media(id=dest_multi.id, media_update=media_update_spec)
        print(response)

        prime_video_mapping[src_multi.media_files.ids[0]] = dest_videos

    # Upload the trip image
    summary_image = "000_summary_trip_image.png"
    for progress, response in tator.util.upload_media(
            api=tator_api, type_id=src_image_type, path=summary_image):
        continue
    print(response)
    summary_image_id = response.id

    summary_media = tator_api.get_media(summary_image_id)
    media_update_spec = {"attributes": summary_media.attributes}
    media_update_spec["attributes"]["tator_user_sections"] = dest_section_tator_user_sections
    response = tator_api.update_media(id=summary_image_id, media_update=media_update_spec)

    # Copy over the GPS states
    #
    # States have shared media IDs. So only loop over the single videos, copy the states in that
    # video, and apply the shared media IDs.
    for src_video_id, dest_video_ids in prime_video_mapping.items():
        states = tator_api.get_state_list(
            project=args.src_project, media_id=[src_video_id], type=src_gps_type)

        # #TODO look into tator.util.clone_state_list to do this
        dest_state_specs = []
        for state in states:
            spec = {
                "type": dest_gps_type,
                "media_ids": dest_video_ids,
                "localization_ids": [],
                "version": state.version,
                **state.attributes
            }
            if state.frame is not None:
                spec["frame"] = state.frame
            dest_state_specs.append(spec)

        if len(states) > 0:
            response = tator_api.create_state_list(project=args.dest_project, state_spec=dest_state_specs)
            print(response)
