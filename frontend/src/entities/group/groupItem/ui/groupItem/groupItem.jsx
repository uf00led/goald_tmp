import { Link } from "react-router-dom";
import defaultGroupImage from "@shared/assets/images/defaultGroupImage.png";

import "./groupItem.scss";

export function GroupItem(props) {
  const { id, avatar = defaultGroupImage, name, tag } = props;

  return (
    <Link to={`/group/${id}`} className="group-item">
      <img src={avatar} className="group-item__avatar" alt="Group Avatar" />
      <div className="group-item__overview">
        <div className="group-item__overview_name">{name}</div>
        {tag && <div className="group-item__overview_tag">{tag}</div>}
      </div>
    </Link>
  );
}
