import { Modal } from "bootstrap";
import { AlertMessage } from "../utils/Alert";

export function InputFormModal({
  modalId,
  title,
  fields,
  formData,
  onChange,
  onSubmit,
  clearForm,
  isEditing,
  submitButtonLabel,
  alert,
}) {
  const closeModal = () => {
    const modalElement = document.getElementById(modalId);
    const modalInstance = Modal.getOrCreateInstance(modalElement);
    modalInstance.hide();
  };

  return (
    <div
      className="modal fade"
      id={modalId}
      tabIndex="-1"
      aria-labelledby={`${modalId}Label`}
      aria-hidden="true"
    >
      <div className="modal-dialog modal-dialog-centered">
        <div className="modal-content">
          <div className="modal-header">
            <h5 className="modal-title" id={`${modalId}Label`}>
              {title}
            </h5>
          </div>
          <form onSubmit={onSubmit}>
            <div className="modal-body">
              {alert && alert.show && (
                <AlertMessage
                  show={alert.show}
                  type={alert.type}
                  message={alert.message}
                />
              )}
              {fields.map((field) => {
                if (field.type === "select") {
                  return (
                    <select
                      key={field.name}
                      name={field.name}
                      className="form-control mb-2"
                      value={formData[field.name]}
                      onChange={onChange}
                      required={field.required}
                      disabled={field.disabled}
                    >
                      <option value="">{field.placeholder}</option>
                      {field.options.map((opt) => (
                        <option key={opt.value} value={opt.value}>
                          {opt.label}
                        </option>
                      ))}
                    </select>
                  );
                } else {
                  return (
                    <input
                      key={field.name}
                      type={field.type}
                      name={field.name}
                      className="form-control mb-2"
                      placeholder={field.placeholder}
                      value={formData[field.name]}
                      onChange={onChange}
                      required={field.required}
                      disabled={field.disabled}
                      min={field.min || undefined}
                      pattern={field.pattern || undefined}
                    />
                  );
                }
              })}
            </div>
            <div className="modal-footer">
              <button
                type="button"
                className="btn btn-outline-dark"
                data-bs-dismiss="modal"
                onClick={() => {
                  clearForm();
                  closeModal();
                }}
              >
                Close
              </button>
              <button type="submit" className="btn btn-outline-primary">
                {submitButtonLabel || (isEditing ? "Update" : "Create")}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}
