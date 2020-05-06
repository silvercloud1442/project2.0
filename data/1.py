

if form.validate_on_submit():
    session = create_session()
    if current_user.id == 1:
        job = session.query(Jobs).filter(Jobs.id == id).first()
    else:
        job = session.query(Jobs).filter(Jobs.id == id,
                                         Jobs.user == current_user).first()
    if job:
        job.customer = current_user.id
        job.title = form.title.data
        job.cost = form.cost.data
        job.description = form.description.data
        job.category = form.category.data
        job.category_2 = form.category_2.data
        UPLOAD_DIR: Path = Path(__file__).parent / 'static/jobs_img'
        UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
        for upload in request.files.getlist('images'):
            filename = secure_filename(upload.filename)
            if filename != '':
                save_path = str(UPLOAD_DIR / filename)
                save_path2 = save_path.split('jobs_img')
                filename = random_name()
                save_path = save_path2[0] + 'jobs_img\\' + filename + '.jpg'
                upload.save(save_path)
                job.img = '\\static\\jobs_img\\{}.jpg'.format(filename)
        session.add(job)
        session.commit()
        return redirect('/')
return render_template('job_add.html', title='Editing', form=form)