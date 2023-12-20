$(document).ready(function () {
    var manager = new Manager();

    function init() {
        manager.init();
    }

    init();

    $(".logo").on("click", () => {
        init();
    });

    $("body").fadeIn("slow");
});

var Group = function (group) {
    var self = this;

    self.id = group.id;
    self.tag = group.tag;
    self.name = group.name;
    self.image = group.image;
    self.leader = group.leader;
    self.is_private = group.is_private;
};

var Goal = function (goal) {
    var self = this;

    self.name = goal;
};

var Event = function (event) {
    var self = this;
}

var Manager = function () {
    var self = this;

    var group_list = new GroupList();
    var group_profile = new GroupProfile();

    var api = new API();

    self.init = function () {
        group_list.init(api.create_group);

        group_list.update(api.get_group_list, function (group_id) {
            group_profile.update(api.get_group_info, group_id);
        });
        //group_profile.update(api.get_full_info);
    };
};

var GroupList = function () {
    var self = this;

    self.init = function (create) {
        $("#create-group-button").on("click", function () {
            create().then(r => self.update());
        });
    };

    self.update = async function (get, action) {
        clear();
        get().then(groups => {
            if (groups) {
                groups.forEach(group => {
                    addGroup(group, action);
                })
            } else {
                addNoGroup();
            }
        });
    };

    function addGroup (group, action) {
        $("#group-list-content").append(element(group, action));
    }

    function addNoGroup () {
        $("group-list-content").append(no_element());
    }

    function clear() {
        $("#group-list-content .list-element").remove();
    }

    function element (group, action) {
        return $("<div>")
            .addClass("list-element button shadow")
            .html(`
                </li>
                    <div class="group-list-image">
                        <img src="${group.image}" alt="group-image">
                    </div>
                    <div class="group-list-info">
                        <h2>${group.name}</h2>
                        <p>${group.tag}</p>
                    </div>
                </li>
            `)
            .bind("click", function () {
                return action(group.id)
            });
    };

    function no_element () {
        return $("<div>")
            .addClass("list-element no-element")
            .html(`
                <h2 class="title">Нет групп</h2>
            `)
    };
};

var GroupProfile = function() {
    var self = this;

    var goals_list = new GoalsList();

    self.update = async function (get, group_id) {
        get(group_id).then(result => {
            showGroup(result["group"]);
            showGoals(result["goals"]);
        });
    };

    function showGroup (group) {
        var showContent = function () {
            $("#entity-info-image").attr("src", group.image);
            $("#entity-info-title").text(group.name + " " + group.tag);
            //$("#entity").fadeIn();
        };

        if ($('#entity').css('display') == 'none') {
            $('#entity').slideDown("fast", showContent);
        } else {
            //$("#entity").fadeOut("fast", showContent);
        }

        showContent();
    }

    function showGoals (goals) {
        goals_list.update(goals);
    }
};

var GoalsList = function() {
    var self = this;

    self.update = function (goals) {
        clear();
        if (goals.length) {
            goals.forEach(goal => addGoal(goal));
        } else {
            addNoGoal();
        }
    };

    function addGoal (goal) {
        $("#goal-list-content").append(element(goal));
    }

    function addNoGoal () {
        $("#goal-list-content").append(no_element());
    }

    function clear () {
        $("#goal-list-content .list-element").remove();
    }

    function element (goal) {
        return $("<div>")
            .addClass("list-element button shadow")
            .html(`
                <div class="goal-list-title">
                    <h2 class="title">${goal.name}</h2>
                </div>
                <div class="goal-list-status">
                    <span class="${goal.is_active ? "active-status" : "notactive-status" }"></span>
                    <p>${goal.is_active ? "активна" : "не активна"}</p>
                </div>
            `);
    };

    function no_element () {
        return $("<div>")
            .addClass("list-element no-element")
            .html(`
                <h2 class="title">Нет целей</h2>
            `)
    }
}

var API = function () {
    var self = this;
    var headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    };

    function get(url) {
        return fetch(url, {
            method: "GET",
            headers: {
                "Accept": "application/json",
            },
        }).then(r => {
                if (r.ok) {
                    return r.json();
                } else {
                    throw new Error(`Bad response: ${r.status} ${r.statusText}`);
                }
            });
    }

    function post(url, data) {
        return fetch(url, {
            method: "POST",
            headers: {...headers},
            body: JSON.stringify(data)
        }).then(r => {
            if (r.ok) {
                return r.json();
            } else {
                return r.json().then(err => {
                    if ("error" in err) {
                        throw new Error(`Bad response: ${err.error}`);
                    }
                }).catch(err => {
                    console.log(err);
                    return err;
                }).then((err) => {
                    if (err == null) {
                        throw new Error(`Bad response: ${r.status} ${r.statusText}`);
                    }
                }).catch(err => {
                    console.log(err);
                    return err;
                })
            }
        });
    }

    self.get_group_list = async function () {
        let groups = await get("group/list")
            .then(g => {
                group_list = [];
                g.forEach(group => {
                    group_list.push(new Group(group));
                })
                return group_list;
            });
        return groups;
    };

    self.get_full_info = async function () {
        return await get("")
    };

    self.get_group_info = async function (group_id) {
        let result = await get(`group/${group_id}`)
            .then(
                r => {
                    var goals = []
                    r.goals.forEach(g => {
                        goals.push(new Goal(g));
                    });
                    return {"group": new Group(r.group), "goals": goals};
                }
            );
        return result;
    };

    self.create_group = async function (group) {
        return await post("group/create", {
            "name": group.name,
            "image": group.image,
            "is_private": group.is_private,
        });
    };
};