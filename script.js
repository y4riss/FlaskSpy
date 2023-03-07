const post = async (imageData) => {

    let formData = new FormData();
    formData.append('stream',imageData);

    fetch("/stream",
    {
        body: formData,
        method: "post"
    });
};

