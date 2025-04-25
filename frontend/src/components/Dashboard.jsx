import { useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import { apiRequest } from "../utils/Apirequest";
import { Edit, Trash2 } from "lucide-react";
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

        console.log("***Logged data***", data);
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
    <div
      className="bg-light py-3 px-4 mb-4 shadow-sm"
      style={{ minHeight: "100vh" }}
    >
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h1 className="h4 mb-0">Hello {user?.user_email}</h1>
        <button className="btn btn-danger" onClick={handleLogout}>
          Logout
        </button>
      </div>

      <div className="card shadow">
        <div className="card-header bg-white d-flex justify-content-between align-items-center py-3">
          <h5 className="mb-0 fw-bold text-primary">Your Tasks</h5>
          <button className="btn btn-primary btn-sm">Add New Task</button>
        </div>

        <div className="card-body p-0">
          <div className="table-responsive">
            <table className="table table-hover mb-0">
              <thead className="table-light">
                <tr>
                  <th className="fw-bold">Title</th>
                  <th className="fw-bold">Description</th>
                  <th className="fw-bold">Category</th>
                  <th className="fw-bold">Due Date</th>
                  <th className="fw-bold">Status</th>
                  <th className="text-end fw-bold">Actions</th>
                </tr>
              </thead>
              <tbody>
                {tasks.length > 0 ? (
                  tasks.map((task) => (
                    <tr key={task.task_id}>
                      <td className="align-middle">{task.task_name}</td>
                      <td className="align-middle">{task.task_desc}</td>
                      <td className="align-middle">{task.task_category}</td>
                      <td className="align-middle">{task.due_date}</td>
                      <td className="align-middle">
                        <span className={getStatusBadgeClass(task.status)}>
                          {task.status}
                        </span>
                      </td>
                      <td className="text-end align-middle">
                        <button
                          className="btn btn-outline-primary btn-sm me-2"
                          onClick={() => handleEdit(task.task_id)}
                        >
                          <Edit className="h-4 w-4" />
                        </button>
                        <button
                          className="btn btn-outline-danger btn-sm"
                          onClick={() => handleDelete(task.task_id)}
                        >
                          <Trash2 className="h-4 w-4" />
                        </button>
                      </td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan="6" className="text-center text-muted py-3">
                      No tasks available.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
