import { useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import { apiRequest } from "../utils/Apirequest";
import "bootstrap-icons/font/bootstrap-icons.css";
import "bootstrap/dist/css/bootstrap.min.css";

function Dashboard() {
  const navigate = useNavigate();
  const user = JSON.parse(localStorage.getItem("current_user"));
  const token = localStorage.getItem("access_token");
  const [tasks, setTasks] = useState([]);


  useEffect(() => {
    const fetchTasks = async () => {
      try {
        const data = await apiRequest({
          url: "http://127.0.0.1:8000/logged-user-tasks",
          method: "GET",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        setTasks(data);
      } catch (err) {
        console.error("Failed to fetch tasks:", err);
      }
    };

    fetchTasks();
  }, []);

  const handleLogout = () => {
    localStorage.clear();
    navigate("/");
  };

  const AddTask = () => {
    console.log("Add Task button clicked!");
    // You can navigate to Add Task page, or open a form/modal
  };

  const handleEdit = (id) => {
    console.log("Edit task:", id);
    // Here you can navigate to an edit page or open a modal
  };

  const handleDelete = (id) => {
    console.log("Delete task:", id);
    // Here you can call an API to delete the task
  };

  const getStatusBadgeClass = (status) => {
    switch (status) {
      case "Completed":
        return "badge bg-success";
      case "In Progress":
        return "badge bg-primary";
      case "Pending":
        return "badge bg-warning";
      case "Not Started":
        return "badge bg-secondary";
      default:
        return "badge bg-info";
    }
  };

  return (
    <div style={{ height: "100vh", width: "100vw" }}>
      <nav className="navbar navbar-expand-md navbar-dark bg-dark">
        <div className="container-fluid">
          <a className="navbar-brand" href="#">
            Welcome {user?.user_email}
          </a>
          <button
            className="navbar-toggler"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#navbarNav"
          >
            <span className="navbar-toggler-icon"></span>
          </button>
          <div className="collapse navbar-collapse" id="navbarNav">
            <ul className="navbar-nav ms-auto">
              <li className="nav-item">
                <a className="nav-link active" href="#">
                  Home
                </a>
              </li>
              <li className="nav-item">
                <a className="nav-link" href="#">
                  Profile
                </a>
              </li>
              <li className="nav-item">
                <a className="nav-link" onClick={handleLogout}>
                  Logout
                </a>
              </li>
            </ul>
          </div>
        </div>
      </nav>

      {/* Dashboard Section */}
      <div className="container my-5">
        <div className="d-flex justify-content-between align-items-center mb-3">
          <h3>Your Task</h3>
          <button className="btn btn-outline-dark" onClick={() => AddTask()}>
            Add Task
          </button>
        </div>
        {/* Table */}
        <div className="table-responsive">
          <table className="table table-striped table-bordered ">
            <thead className="table-dark">
              <tr>
                <th className="fw-bold">Title</th>
                <th className="fw-bold">Description</th>
                <th className="fw-bold">Category</th>
                <th className="fw-bold">Assigned Date</th>
                <th className="fw-bold">Due Date</th>
                <th className="fw-bold">Status</th>
                <th className="fw-bold">Actions</th>
              </tr>
            </thead>
            <tbody>
              {tasks.length > 0 ? (
                tasks.map((task) => (
                  <tr key={task.task_id}>
                    <td className="align-middle">{task.task_name}</td>
                    <td className="align-middle">{task.task_desc}</td>
                    <td className="align-middle">{task.task_category}</td>
                    <td className="align-middle">{task.assigned_date}</td>
                    <td className="align-middle">{task.due_date}</td>
                    <td className="align-middle">
                      <span className={getStatusBadgeClass(task.status)}>
                        {task.status}
                      </span>
                    </td>
                    <td className="text-end align-middle">
                      <i
                        className="bi bi-pencil me-3"
                        onClick={() => handleEdit(task.task_id)}
                      ></i>
                      <i
                        className="bi bi-trash"
                        onClick={() => handleDelete(task.task_id)}
                      ></i>
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan="7" className="text-center text-muted py-3">
                    No tasks available.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
