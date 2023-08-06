import numpy as np

#tests = [10]
tests = range(0,9)
#tests = [10]
tests = range(1,2)
#tests = [8]

for tn in tests:

    if tn == 0:
        # GUI plot of timeseries and spectra
        from hapiclient import hapi
        from hapiclient import hapiplot

        server     = 'http://hapi-server.org/servers/TestData2.0/hapi'
        dataset    = 'dataset1'
        parameters = 'scalar,spectra'
        start      = '1970-01-01Z'
        stop       = '1970-01-01T00:00:11Z'
        opts       = {'logging': True, 'usecache': False}

        data, meta = hapi(server, dataset, parameters, start, stop, **opts)
        meta = hapiplot(data, meta, **opts)

    if tn == 1 or tn == 2:
        # Compare png with GUI plot
        import io
        from PIL import Image

        from hapiclient import hapi
        from hapiclient import hapiplot

        server     = 'http://hapi-server.org/servers/TestData2.0/hapi'
        dataset    = 'dataset1'
        start      = '1970-01-01Z'
        stop       = '1970-01-01T00:00:11Z'
        parameters = 'scalar'
        opts       = {'logging': False, 'usecache': False}
        popts      = {'useimagecache': False, 'logging': True, 'returnimage':True}

        if tn == 1:
            # returnimage=True for scalar parameter - compare with GUI plot
            parameters = 'scalar'
            data, meta = hapi(server, dataset, parameters, start, stop, **opts)
            meta = hapiplot(data, meta, **popts)
            img = meta['parameters'][1]['hapiplot']['image']
            Image.open(io.BytesIO(img)).show()

            hapiplot(data, meta)

        if tn == 2:
            # returnimage=True for heatmap parameter - compare with GUI plot
            parameters = 'spectra'
            data, meta = hapi(server, dataset, parameters, start, stop, **opts)
            meta = hapiplot(data, meta, **popts)
            img = meta['parameters'][1]['hapiplot']['image']
            Image.open(io.BytesIO(img)).show()

            hapiplot(data, meta)

    if tn == 3:
        # returned image should be same independent of saveimage
        import io
        from PIL import Image

        from hapiclient import hapi
        from hapiclient import hapiplot

        server     = 'http://hapi-server.org/servers/TestData2.0/hapi'
        dataset    = 'dataset1'
        start      = '1970-01-01Z'
        stop       = '1970-01-01T00:00:11Z'
        parameters = 'scalar'
        opts       = {'logging': False, 'usecache': True}
        data, meta = hapi(server, dataset, parameters, start, stop, **opts)

        popts = {
                     'usecache': True,
                     'useimagecache': False,
                     'logging': True,
                     'saveimage': False,
                     'returnimage':True
                 }

        meta = hapiplot(data, meta, **popts)
        img1 = meta['parameters'][1]['hapiplot']['image']
        Image.open(io.BytesIO(img1)).show()

        popts['saveimage'] = True
        meta = hapiplot(data, meta, **popts)
        img2 = meta['parameters'][1]['hapiplot']['image']
        Image.open(io.BytesIO(img1)).show()

        if img1 != img2:
            raise ValueError('Images do not match')

    if tn == 4:
        # Transparency
        import io
        from PIL import Image

        from hapiclient import hapi
        from hapiclient import hapiplot

        server     = 'http://hapi-server.org/servers/TestData2.0/hapi'
        dataset    = 'dataset1'
        start      = '1970-01-01Z'
        stop       = '1970-01-01T00:00:11Z'
        parameters = 'scalar'
        opts       = {'logging': False, 'usecache': True}
        data, meta = hapi(server, dataset, parameters, start, stop, **opts)

        popts = {
                    'usecache': True,
                    'useimagecache': False,
                    'logging': True,
                    'saveimage': True,
                    'returnimage': True
                 }

        meta = hapiplot(data, meta, **popts)
        img = meta['parameters'][1]['hapiplot']['image']
        Image.open(io.BytesIO(img)).show()

        popts['rcParams'] = {'savefig.transparent': False}
        meta = hapiplot(data, meta, **popts)
        img = meta['parameters'][1]['hapiplot']['image']
        Image.open(io.BytesIO(img)).show()

    if tn == 5:
        # Rc params
        import io
        from PIL import Image

        from hapiclient import hapi
        from hapiclient import hapiplot

        server     = 'http://hapi-server.org/servers/TestData2.0/hapi'
        dataset    = 'dataset1'
        start      = '1970-01-01Z'
        stop       = '1970-01-01T00:00:11Z'
        parameters = 'scalar'
        opts       = {'logging': False, 'usecache': True}
        data, meta = hapi(server, dataset, parameters, start, stop, **opts)

        popts = {
                    'usecache': True,
                    'useimagecache': False,
                    'logging': True,
                    'saveimage': True,
                    'returnimage': True,
                    'rcParams': {
                        'savefig.transparent': False,
                        'figure.facecolor': 'black',
                        'savefig.facecolor': 'black',
                        'text.color': 'yellow',
                        'xtick.color': 'yellow',
                        'ytick.color': 'yellow',
                        'axes.labelcolor': 'yellow'
                    }
                 }

        meta = hapiplot(data, meta, **popts)
        img = meta['parameters'][1]['hapiplot']['image']
        Image.open(io.BytesIO(img)).show()

        popts['returnimage'] = False
        hapiplot(data, meta, **popts)

    if tn == 6:
        # Style and rc parameters before and after + tight layout
        from hapiclient import hapi
        from hapiclient import hapiplot

        server     = 'http://hapi-server.org/servers/TestData2.0/hapi'
        dataset    = 'dataset1'
        parameters = 'vector'
        start      = '1970-01-01Z'
        stop       = '1970-01-01T00:00:11Z'
        opts       = {'logging': True, 'usecache': False}

        #https://matplotlib.org/gallery/style_sheets/style_sheets_reference.html
        #https://tonysyu.github.io/raw_content/matplotlib-style-gallery/gallery.html
        import matplotlib
        rclib =  matplotlib.style.library
        print('Style options available:')
        for key in rclib:
            print(key)

        popts = {
                    'logging': True,
                    'saveimage': False,
                    'style': 'classic'
                }

        data, meta = hapi(server, dataset, parameters, start, stop, **opts)

        if matplotlib.get_backend() in matplotlib.rcsetup.interactive_bk:
            # Set labels and make tight layout after call to hapiplot
            meta = hapiplot(data, meta, **popts)
            fig = meta['parameters'][1]['hapiplot']['figure']
            fig.axes[0].set_ylabel('y label\nsub y label\nsub sub ylabel')
            fig.tight_layout()
            fig.show()
            # Two calls to fig.tight_layout() may be needed b/c of bug in PyQt:
            # https://github.com/matplotlib/matplotlib/issues/10361

            # Set labels and make tight in call to hapiplot
            popts['_rcParams'] = {'figure.bbox': 'tight'}
            popts['ylabel'] = 'y label\nsub y label\nsub sub ylabel 2'
            meta = hapiplot(data, meta, **popts)
        else:
            print("Skipping test because matplotlib backend is not interactive.")


    if tn == 7:
        from hapiclient import hapi
        from hapiclient import hapiplot

        # Spectra from CASSINIA S/C
        server     = 'http://datashop.elasticbeanstalk.com/hapi';
        dataset    = 'CHEMS_PHA_BOX_FLUXES_FULL_TIME_RES';
        parameters = 'HPlus_BEST_T1';
        start      = '2004-07-01T04:00:00Z';
        stop       = '2004-07-01T06:00:00Z';
        opts       = {'logging': True, 'usecache': True}
        data,meta  = hapi(server, dataset, parameters, start, stop, **opts)

        popts = {'logging': True, 'logy': True, 'logz': True}
        hapiplot(data, meta, **popts)

    if tn == 8:
        from hapiclient import hapi
        from hapiclient import hapiplot

        # Spectra w/ only bin centers and different timeStampLocations
        server     = 'http://hapi-server.org/servers/TestData2.0/hapi'
        dataset    = 'dataset1'
        start      = '1970-01-01Z'
        stop       = '1970-01-01T00:00:11Z'
        parameters = 'spectra'
        opts       = {'logging': True, 'usecache': True}
        data, meta = hapi(server, dataset, parameters, start, stop, **opts)

        popts = {'logging': True}

        data['spectra'][3,3] = -1e31 # Add a fill value

        # Default
        hapiplot(data, meta, **popts)

        # Should be same as previous plot
        meta['timeStampLocation'] = 'center'
        hapiplot(data, meta, **popts)

        meta['timeStampLocation'] = 'begin'
        hapiplot(data, meta, **popts)

        meta['timeStampLocation'] = 'end'
        hapiplot(data, meta, **popts)

        # Remove 6th time value so cadence is not uniform
        # Missing time value is at 00:00:06. Note that data at this time
        # takes on the value of data at 00:00:05. If we knew the bin,
        # width was uniform, values at 00:00:06 could be set as NaN.
        # heatmap does not assume the bin width is uniform. Some software
        # will assume bin width is uniform and equal to the difference
        # between timestamps.
        data = np.delete(data, 6, 0)

        meta['timeStampLocation'] = 'begin'
        hapiplot(data, meta, **popts)

        meta['timeStampLocation'] = 'end'
        hapiplot(data, meta, **popts)

        meta['timeStampLocation'] = 'center'
        hapiplot(data, meta, **popts)

    if tn == 9:
        # All TestData2.0 parameters
        from hapiclient import hapi
        from hapiclient import hapiplot

        server     = 'http://localhost:9998/TestData2.0/hapi'
        dataset    = 'dataset1'
        start      = '1970-01-01Z'
        stop       = '1970-01-01T00:00:11Z'
        opts       = {'logging': True, 'usecache': False}

        meta = hapi(server, dataset, **opts)
        for i in range(0,len(meta['parameters'])):
            parameter  = meta['parameters'][i]['name']
            data, metax = hapi(server, dataset, parameter, start, stop, **opts)
            if i > 0: # Time parameter alone when i = 0. No fill allowed for time parameter.
                # Change fill value to be same as second element of parameter array.
                metax["parameters"][1]['fill'] = data[parameter].take(1).astype('U')
            hapiplot(data, metax, **opts)

    if tn == 10:
        # All TestData2.1 parameters
        from hapiclient import hapi
        from hapiclient import hapiplot

        server     = 'http://localhost:9998/TestData2.1/hapi'
        dataset    = 'dataset1'
        start      = '1970-01-01Z'
        stop       = '1970-01-01T00:00:11Z'
        opts       = {'logging': True, 'usecache': False}

        meta = hapi(server1, dataset, **opts)
        for i in range(0,len(meta['parameters'])):
            parameter  = meta['parameters'][i]['name']
            data, metax = hapi(server, dataset, parameter, start, stop, **opts)
            if i > 0: # Time parameter alone when i = 0. No fill allowed for time parameter.
                # Change fill value to be same as second element of parameter array.
                metax["parameters"][1]['fill'] = data[parameter].take(1).astype('U')
            hapiplot(data, metax, **opts)        