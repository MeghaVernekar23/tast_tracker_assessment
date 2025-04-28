import { useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import { apiRequest } from "../utils/Apirequest";
import "bootstrap-icons/font/bootstrap-icons.css";
import "bootstrap/dist/css/bootstrap.min.css";
import { Modal } from "bootstrap";

function Dashboard() {
  const navigate = useNavigate();
  const user = JSON.parse(localStorage.getItem("current_user"));
  const token = localStorage.getItem("access_token");
  const [tasks, setTasks] = useState([]);
  const [taskAlert, setTaskAlert] = useState({
    show: false,
    message: "",
    type: "success",
  });
  const showAlert = (message, type = "success") => {
    setTaskAlert({
      show: true,
      message: message,
      type: type,
    });

    setTimeout(() => {
      setTaskAlert({
        show: false,
        message: "",
        type: "success",
      });
    }, 2000);
  };

  const [addTaskData, setAddTaskData] = useState({
    task_name: "",
    task_desc: "",
    task_category: "",
    due_date: "",
    status: "",
  });

  const [editingTaskId, setEditingTaskId] = useState(null);

  const [deleteTaskId, setdeleteTaskId] = useState(null);

  useEffect(() => {
    fetchTasks();
  }, []);

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

  const handleLogout = () => {
    localStorage.clear();
    navigate("/");
  };

  const addUpdateTask = async (e) => {
    e.preventDefault();
    if (editingTaskId) {
      editTask();
    } else {
      addTask();
    }
  };

  const addTask = async () => {
    try {
      await apiRequest({
        url: "http://localhost:8000/addTask",
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
        },
        body: {
          task_name: addTaskData.task_name,
          task_desc: addTaskData.task_desc,
          task_category: addTaskData.task_category,
          due_date: addTaskData.due_date,
        },
      });
      closeModal("addTaskModal");
      await fetchTasks();
      showAlert("Task Added Successfully !!", "success");
      clearAddTaskForm();
    } catch {
      showAlert("Error occured while adding the task.");
    }
  };

  const editTask = async () => {
    try {
      await apiRequest({
        url: `http://localhost:8000/UpdateTask/${editingTaskId}`,
        method: "PUT",
        headers: {
          Authorization: `Bearer ${token}`,
        },
        body: {
          task_name: addTaskData.task_name,
          task_desc: addTaskData.task_desc,
          task_category: addTaskData.task_category,
          due_date: addTaskData.due_date,
          status: addTaskData.status,
        },
      });
      closeModal("addTaskModal");
      await fetchTasks();
      showAlert("Task Updated Successfully !!", "success");
    } catch {
      showAlert("Error occured while updating the task");
    }
  };

  const handleAddTaskChange = (e) => {
    setAddTaskData({ ...addTaskData, [e.target.name]: e.target.value });
  };

  const clearAddTaskForm = () => {
    setAddTaskData({
      task_name: "",
      task_desc: "",
      task_category: "",
      due_date: "",
    });
  };

  const handleEdit = (taskId) => {
    console.log("Edit task:", taskId);
    const taskToEdit = tasks.find((task) => task.task_id === taskId);
    if (taskToEdit) {
      setAddTaskData({
        task_name: taskToEdit.task_name,
        task_desc: taskToEdit.task_desc,
        task_category: taskToEdit.task_category,
        due_date: taskToEdit.due_date.split("T")[0],
        status: taskToEdit.status || "",
      });
      setEditingTaskId(taskId);

      const modalElement = document.getElementById("addTaskModal");
      const modalInstance = Modal.getOrCreateInstance(modalElement);
      modalInstance.show();
    }
  };

  const handleDelete = (taskId) => {
    console.log("Delete task:", taskId);

    setdeleteTaskId(taskId);
    const modalElement = document.getElementById("deleteTaskModal");
    const modalInstance = Modal.getOrCreateInstance(modalElement);
    modalInstance.show();
  };

  const deleteTask = async (e) => {
    e.preventDefault();
    try {
      await apiRequest({
        url: `http://localhost:8000/deleteTask/${deleteTaskId}`,
        method: "DELETE",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      closeModal("deleteTaskModal");
      await fetchTasks();
      showAlert("Task Deleted Successfully !!", "success");
    } catch {
      showAlert("Error occured while deleting the task");
    }
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

  const closeModal = (modalId) => {
    const modalElement = document.getElementById(modalId);
    const modalInstance = Modal.getOrCreateInstance(modalElement);
    modalInstance.hide();

    const modalBackdrop = document.querySelector(".modal-backdrop");
    if (modalBackdrop) {
      modalBackdrop.remove();
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

      <div className="container my-5">
        {taskAlert.show && (
          <div className={`alert alert-${taskAlert.type} mt-3`} role="alert">
            {taskAlert.message}
          </div>
        )}
        <div className="d-flex justify-content-between align-items-center mb-3">
          <h3>Your Task</h3>
          <button
            className="btn btn-outline-dark"
            data-bs-toggle="modal"
            data-bs-target="#addTaskModal"
            onClick={() => {
              clearAddTaskForm();
              setEditingTaskId(null);
            }}
          >
            Add Task
          </button>
        </div>
        <div className="table-responsive">
          <table className="table table-striped table-bordered ">
            <thead className="table-dark">
              <tr>
                <th className="fw-bold">Name</th>
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
        <div
          className="modal fade"
          id="addTaskModal"
          tabIndex="-1"
          aria-labelledby="addTaskModalLabel"
          aria-hidden="true"
        >
          <div className="modal-dialog modal-dialog-centered">
            <div className="modal-content">
              {editingTaskId !== null ? (
                <div className="modal-header">
                  <h5 className="modal-title" id="addTaskModalLabel">
                    Edit Task
                  </h5>
                </div>
              ) : (
                <div className="modal-header">
                  <h5 className="modal-title" id="addTaskModalLabel">
                    Add Task
                  </h5>
                </div>
              )}

              <form onSubmit={addUpdateTask}>
                <div className="modal-body">
                  <input
                    type="text"
                    name="task_name"
                    className="form-control mb-2"
                    placeholder="Taskname"
                    value={addTaskData.task_name}
                    onChange={handleAddTaskChange}
                    required
                    disabled={editingTaskId !== null}
                  />
                  <input
                    type="text"
                    name="task_desc"
                    className="form-control mb-2"
                    placeholder="Task Description"
                    value={addTaskData.task_desc}
                    onChange={handleAddTaskChange}
                    required
                  />
                  <select
                    name="task_category"
                    className="form-control mb-2"
                    value={addTaskData.task_category}
                    onChange={handleAddTaskChange}
                    required
                    disabled={editingTaskId !== null}
                  >
                    <option value="">Select Category</option>
                    <option value="fitness">Fitness</option>
                    <option value="study">Study</option>
                    <option value="others">Others</option>
                  </select>
                  <input
                    type="date"
                    name="due_date"
                    className="form-control mb-2"
                    placeholder="Task Due Date"
                    value={addTaskData.due_date}
                    onChange={handleAddTaskChange}
                    min={new Date().toISOString().split("T")[0]}
                    required
                  />
                  {editingTaskId !== null && (
                    <select
                      name="status"
                      className="form-control mb-2"
                      value={addTaskData.status}
                      onChange={handleAddTaskChange}
                      required
                    >
                      <option value="">Select Status</option>
                      <option value="Pending">Pending</option>
                      <option value="In Progress">In Progress</option>
                      <option value="Completed">Completed</option>
                    </select>
                  )}
                  <div className="modal-footer">
                    <button
                      type="button"
                      className="btn btn-outline-dark"
                      data-bs-dismiss="modal"
                      onClick={() => {
                        clearAddTaskForm();
                        fetchTasks();
                      }}
                    >
                      Close
                    </button>
                    {editingTaskId !== null ? (
                      <button type="submit" className="btn btn-outline-primary">
                        Edit Task
                      </button>
                    ) : (
                      <button type="submit" className="btn btn-outline-primary">
                        Add Task
                      </button>
                    )}
                  </div>
                </div>
              </form>
            </div>
          </div>
        </div>
        <div
          className="modal fade"
          id="deleteTaskModal"
          tabIndex="-1"
          aria-labelledby="deleteTaskModalLabel"
          aria-hidden="true"
        >
          <div className="modal-dialog modal-dialog-centered">
            <div className="modal-content">
              <div className="modal-header">
                <h5 className="modal-title" id="deleteTaskModalLabel">
                  Delete Task
                </h5>
              </div>

              <form onSubmit={deleteTask}>
                <div className="modal-body">
                  <h5>Are you sure you want to delete the task</h5>

                  <div className="modal-footer">
                    <button
                      type="button"
                      className="btn btn-outline-dark"
                      data-bs-dismiss="modal"
                      onClick={() => {
                        fetchTasks();
                      }}
                    >
                      Close
                    </button>
                    <button type="submit" className="btn btn-outline-primary">
                      Delete Task
                    </button>
                  </div>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
